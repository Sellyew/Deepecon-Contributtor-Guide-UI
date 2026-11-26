"""M3: guidance, resumable uploads with a SHA-256 receipt, dataset routes, the public-reference
option, numbered submissions, the manifest export, and the team's pages (plan §2.5, §5; MVP §5)."""
import hashlib
import io
import json
import os
import stat
import zipfile
from pathlib import Path
from unittest import mock

from django.core.management import call_command

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from contributors.models import Assignment, Consent
from contributors.tests import ContributorSiteTestCase
from papers.importers import _validator
from papers.models import EventLog

from . import manifest, storage
from .models import Submission, SubmissionVersion, Upload


def make_zip(files=None):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, content in (files or {"README.md": "Fictional README", "code/run_all.do": "* fictional"}).items():
            archive.writestr(name, content)
    return buffer.getvalue()


class SubmissionTestCase(ContributorSiteTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.pid = self.empirical.paper_id

    def url(self, name, *args, paper_id=None):
        return reverse(f"submissions:{name}", args=[paper_id or self.pid, *args])

    def start(self, name="package.zip", size=None, data=None, client=None, modified=1700000000000, paper_id=None):
        """What upload.js sends: name, size, last-modified time, and the SHA-256 of the first MiB."""
        data = data if data is not None else make_zip()
        head = hashlib.sha256(data[:storage.HEAD_BYTES]).hexdigest()
        response = (client or self.client).post(self.url("upload_start", paper_id=paper_id),
                                                {"name": name, "size": size or len(data), "modified": modified, "head": head},
                                                HTTP_X_REQUESTED_WITH="fetch")
        return response, data

    def chunk(self, upload_id, offset, body, client=None, paper_id=None):
        return (client or self.client).post(f"{self.url('upload_chunk', upload_id, paper_id=paper_id)}?offset={offset}", body,
                                            content_type="application/octet-stream", HTTP_X_REQUESTED_WITH="fetch")

    def upload(self, data=None, name="package.zip"):
        response, data = self.start(name=name, data=data)
        body = response.json()
        return self.chunk(body["id"], 0, data).json(), data

    def form(self, **overrides):
        """A complete empirical submission by upload, as the form posts it."""
        sub = manifest.submission_for(self.a_emp)
        data = {"channel": "upload", "master_script": "code/run_all.do", "readme": "README.md", "software": "Stata, 18",
                "dependencies_included": "yes", "author_run_log_included": "yes", "expected_outputs_included": "yes",
                "run_time": "1-2 hours", "no_restricted_included": "on", "version": str(sub.version),
                "datasets-TOTAL_FORMS": "1", "datasets-INITIAL_FORMS": "0", "datasets-MIN_NUM_FORMS": "0",
                "datasets-MAX_NUM_FORMS": "50",
                "datasets-0-name": "Fictional student records", "datasets-0-availability": "restricted_not_included",
                "datasets-0-access_route": "author_runs_and_returns_outputs", "datasets-0-source": "Fictional agency"}
        for entry in self.empirical.config["materials_checklist"]:
            data[f"status_{entry['id']}"] = "provided" if entry["requirement"] != "optional" else ""
        data.update(overrides)
        return {k: v for k, v in data.items() if v is not None}


class GuidancePage(SubmissionTestCase):
    def test_shows_the_papers_checklist_routes_and_the_ai_rules(self):
        page = self.client.get(self.url("guidance"))
        for entry in self.empirical.config["materials_checklist"]:
            self.assertContains(page, entry["label"]["en"])
        self.assertContains(page, "Restricted or confidential")
        self.assertContains(page, "Never put restricted, confidential, or licensed data into any AI tool.")
        self.assertContains(page, "example-archive 000000, V1")          # the public package from the configuration

    def test_a_theory_paper_gets_its_own_checklist_and_no_data_section(self):
        bo = self.client_class()
        self.open_link(self.bo_token, client=bo)
        bo.post(reverse("contributors:notice", args=[self.theory.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        bo.post(reverse("set_language"), {"language": "en", "next": "/"})
        page = bo.get(self.url("guidance", paper_id=self.theory.paper_id))
        self.assertContains(page, "LaTeX source of the paper and appendix")
        self.assertNotContains(page, "Restricted or confidential")
        self.assertNotContains(page, "public package's reference")      # the theory paper accepts uploads only

    def test_needs_consent_and_the_current_paper(self):
        self.assertEqual(self.client.get(self.url("guidance", paper_id=self.theory.paper_id)).status_code, 404)
        Consent.objects.filter(assignment=self.a_emp).delete()
        self.assertRedirects(self.client.get(self.url("guidance")), reverse("contributors:notice", args=[self.pid]))
        self.assertRedirects(self.client.get(self.url("submit")), reverse("contributors:notice", args=[self.pid]))

    def test_the_overview_links_to_the_materials(self):
        page = self.client.get(reverse("contributors:my_paper", args=[self.pid]))
        self.assertContains(page, self.url("guidance"))
        self.assertContains(page, self.url("submit"))

    def test_the_guidance_is_bilingual(self):
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": "/"})
        page = self.client.get(self.url("guidance"))
        self.assertContains(page, "使用 AI 工具")
        self.assertContains(page, "遵循期刊数据编辑模板的 README")        # the checklist's own Chinese label
        self.assertNotContains(page, "Materials guidance")


class Uploads(SubmissionTestCase):
    def test_chunks_are_received_and_the_receipt_is_the_files_sha256(self):
        data = make_zip()
        with override_settings(UPLOAD_CHUNK_BYTES=100):
            response, _ = self.start(data=data)
            self.assertEqual(response.status_code, 201)
            body = response.json()
            offset = 0
            while offset < len(data):
                body = self.chunk(body["id"], offset, data[offset:offset + 100]).json()
                offset = body["offset"]
        self.assertEqual(body["status"], "received")
        self.assertEqual(body["sha256"], hashlib.sha256(data).hexdigest())
        upload = Upload.objects.get()
        self.assertEqual(sorted(name for name, _size in upload.entries), ["README.md", "code/run_all.do"])
        path = storage.path_of(upload)
        self.assertTrue(path.is_file())
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertTrue(path.is_relative_to(Path(self.private_root).resolve()))
        self.assertEqual(sorted(p.name for p in path.parent.iterdir()), [path.name])      # nothing extracted
        page = self.client.get(self.url("submit"))
        self.assertContains(page, upload.sha256)

    def test_an_interrupted_upload_resumes_where_it_stopped(self):
        data = make_zip({"data/big.bin": os.urandom(3 * 1024 * 1024)})
        step = 1024 * 1024
        with override_settings(UPLOAD_CHUNK_BYTES=step):
            first = self.start(data=data)[0].json()
            self.chunk(first["id"], 0, data[:step])
            self.chunk(first["id"], step, data[step:2 * step])
            again = self.start(data=data)[0].json()                  # the same file chosen again
            self.assertEqual((again["id"], again["offset"]), (first["id"], 2 * step))
            repeated = self.chunk(first["id"], step, data[step:2 * step])    # a chunk sent twice is not written twice
            self.assertEqual((repeated.status_code, repeated.json()["offset"]), (409, 2 * step))
            offset = 2 * step
            while offset < len(data):
                body = self.chunk(first["id"], offset, data[offset:offset + step]).json()
                offset = body["offset"]
        self.assertEqual(body["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(Upload.objects.count(), 1)

    def test_a_different_file_with_the_same_name_and_size_is_never_joined(self):
        one = make_zip({"data/a.bin": os.urandom(2 * 1024 * 1024)})
        two = make_zip({"data/a.bin": os.urandom(2 * 1024 * 1024)})
        self.assertEqual(len(one), len(two))
        with override_settings(UPLOAD_CHUNK_BYTES=1024 * 1024 + 512):
            first = self.start(data=one)[0].json()
            self.chunk(first["id"], 0, one[:1024 * 1024 + 512])
            other_time = self.start(data=one, modified=1)[0].json()          # another last-modified time
            other_bytes = self.start(data=two)[0].json()                     # same time, other first MiB
        self.assertNotIn(first["id"], (other_time["id"], other_bytes["id"]))
        self.assertEqual((other_time["offset"], other_bytes["offset"]), (0, 0))

    def test_refusals(self):
        self.assertEqual(self.start(name="package.tar.gz")[0].status_code, 400)
        with override_settings(DEFAULT_MAX_UPLOAD_BYTES=10):
            config = dict(self.empirical.config, submission={"accepted_channels": ["upload"]})
            self.empirical.config = config
            self.empirical.save()
            refused = self.start()[0]
            self.assertEqual(refused.json()["error"], "too_large")
        self.empirical.config["submission"] = {"accepted_channels": ["upload"], "max_upload_bytes": 10 ** 6}
        self.empirical.save()
        body, _ = self.upload(data=b"not a zip archive at all")
        self.assertEqual(body["status"], "refused")
        self.assertFalse(any((Path(self.private_root) / "uploads").rglob("*.zip")))   # not kept
        with override_settings(UPLOAD_CHUNK_BYTES=10):
            started = self.start(name="other.zip")[0].json()
            self.assertEqual(self.chunk(started["id"], 0, b"x" * 11).status_code, 400)

    def test_the_form_without_javascript_uploads_the_whole_file(self):
        data = make_zip()
        response = self.client.post(self.url("upload_plain"), {"package": SimpleUploadedFile("pkg.zip", data)}, follow=True)
        self.assertContains(response, hashlib.sha256(data).hexdigest())
        self.assertEqual(Upload.objects.get().status, Upload.RECEIVED)

    def test_other_contributors_and_papers_cannot_reach_an_upload(self):
        started = self.start()[0].json()
        bo = self.client_class()
        self.open_link(self.bo_token, client=bo)
        bo.post(reverse("contributors:notice", args=[self.theory.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        tid = self.theory.paper_id
        self.assertEqual(self.chunk(started["id"], 0, b"x", client=bo, paper_id=self.pid).status_code, 404)
        self.assertEqual(self.chunk(started["id"], 0, b"x", client=bo, paper_id=tid).status_code, 404)
        self.assertEqual(bo.get(self.url("upload_status", started["id"], paper_id=tid)).status_code, 404)
        self.assertEqual(bo.post(self.url("upload_remove", started["id"], paper_id=tid)).status_code, 404)
        self.assertEqual(Upload.objects.get().received_bytes, 0)

    def test_uploads_need_the_upload_channel(self):
        self.empirical.config["submission"] = {"accepted_channels": ["public_reference"]}
        self.empirical.save()
        self.assertEqual(self.start()[0].status_code, 404)

    def test_an_upload_can_be_removed_until_it_is_submitted(self):
        body, _ = self.upload()
        upload = Upload.objects.get(public_id=body["id"])
        self.client.post(self.url("upload_remove", upload.public_id))
        self.assertFalse(Upload.objects.exists())
        self.assertFalse(any((Path(self.private_root) / "uploads").rglob("*.zip")))
        self.upload()
        self.client.post(self.url("submit"), self.form(submit="1"))
        kept = Upload.objects.get()
        self.client.post(self.url("upload_remove", kept.public_id))
        self.assertTrue(Upload.objects.filter(pk=kept.pk).exists())                # part of version 1

    def test_logs_hold_sizes_and_hashes_not_file_names(self):
        self.upload(data=make_zip({"secret-name-of-a-dataset.csv": "1"}))
        self.assertNotIn("secret-name-of-a-dataset", json.dumps(list(EventLog.objects.values_list("details", flat=True))))


class Submitting(SubmissionTestCase):
    def test_a_draft_is_saved_and_nothing_is_submitted(self):
        response = self.client.post(self.url("submit"), self.form(save="1"), follow=True)
        self.assertContains(response, "Saved as a draft.")
        self.assertFalse(SubmissionVersion.objects.exists())
        self.assertEqual(Submission.objects.get().master_script, "code/run_all.do")

    def test_submitting_needs_every_required_answer(self):
        page = self.client.post(self.url("submit"), self.form(submit="1", no_restricted_included=None))
        self.assertContains(page, "Upload your package")
        self.assertContains(page, "Confirm that nothing restricted or confidential is included.")
        self.assertFalse(SubmissionVersion.objects.exists())

    def test_a_complete_submission_is_a_numbered_version_with_a_valid_manifest(self):
        _, data = self.upload()
        self.client.post(self.url("submit"), self.form(submit="1"))
        version = SubmissionVersion.objects.get()
        self.assertEqual(version.version, 1)
        self.assertEqual(list(_validator("submission-manifest").iter_errors(version.manifest)), [])
        self.assertEqual(version.manifest["files"][0]["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(version.manifest["datasets"][0]["access_route"], "author_runs_and_returns_outputs")
        self.assertEqual(version.manifest_sha256, manifest.canonical_sha256(version.manifest))
        self.assertTrue(EventLog.objects.filter(operation="submission_submitted").exists())
        self.client.post(self.url("submit"), self.form(submit="1", run_time="2-8 hours"))
        self.assertEqual(list(SubmissionVersion.objects.values_list("version", flat=True)), [1, 2])

    def test_restricted_data_need_a_route_and_public_data_a_place(self):
        page = self.client.post(self.url("submit"), self.form(save="1", **{"datasets-0-access_route": ""}))
        self.assertContains(page, "need a route")
        page = self.client.post(self.url("submit"), self.form(save="1", **{"datasets-0-availability": "public_elsewhere",
                                                                          "datasets-0-access_route": ""}))
        self.assertContains(page, "Say where the public data are.")
        self.assertFalse(Submission.objects.filter(master_script="code/run_all.do").exists())

    def test_included_data_need_permission_to_share(self):
        self.upload()
        page = self.client.post(self.url("submit"), self.form(submit="1", **{"datasets-0-availability": "included",
                                                                            "datasets-0-access_route": ""}))
        self.assertContains(page, "Confirm that you may share the data you include")
        self.client.post(self.url("submit"), self.form(submit="1", permission_to_share="on",
                                                       **{"datasets-0-availability": "included", "datasets-0-access_route": ""}))
        version = SubmissionVersion.objects.get()
        self.assertTrue(version.manifest["declarations"]["permission_to_share_included_data"])

    def test_the_public_reference_works_without_an_upload(self):
        page = self.client.get(self.url("submit"))
        self.assertEqual(page.context["form"].initial["pub_repository"], "example-archive")      # from the configuration
        self.client.post(self.url("submit"), self.form(submit="1", channel="public_reference", pub_repository="example-archive",
                                                       pub_identifier="000000", pub_version="V1"))
        version = SubmissionVersion.objects.get()
        self.assertEqual(version.manifest["public_reference"]["identifier"], "000000")
        self.assertNotIn("files", version.manifest)

    def test_a_stale_page_does_not_overwrite_newer_answers(self):
        self.client.post(self.url("submit"), self.form(save="1"))
        stale = self.form(save="1", version="0", master_script="old.do")
        response = self.client.post(self.url("submit"), stale, follow=True)
        self.assertContains(response, "saved from another tab")
        self.assertEqual(Submission.objects.get().master_script, "code/run_all.do")

    def test_a_theory_paper_needs_no_package_block(self):
        bo = self.client_class()
        self.open_link(self.bo_token, client=bo)
        bo.post(reverse("contributors:notice", args=[self.theory.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        tid = self.theory.paper_id
        data = make_zip({"paper.tex": "\\documentclass{article}"})
        start = bo.post(self.url("upload_start", paper_id=tid), {"name": "sources.zip", "size": len(data)}).json()
        self.chunk(start["id"], 0, data, client=bo, paper_id=tid)
        # Exactly what the real page posts: it has no datasets section, so no dataset fields at all.
        page = bo.get(self.url("submit", paper_id=tid)).content.decode()
        self.assertNotIn("datasets-TOTAL_FORMS", page)
        form = {"channel": "upload", "no_restricted_included": "on", "version": "0", "status_source": "provided",
                "status_file-names": "provided", "submit": "1"}
        bo.post(self.url("submit", paper_id=tid), form)
        version = SubmissionVersion.objects.get(assignment=self.b_th)
        self.assertNotIn("package", version.manifest)
        self.assertEqual(list(_validator("submission-manifest").iter_errors(version.manifest)), [])

    def test_the_overview_shows_the_latest_submission(self):
        self.upload()
        self.client.post(self.url("submit"), self.form(submit="1"))
        self.assertContains(self.client.get(reverse("contributors:my_paper", args=[self.pid])), "Submitted: version 1")


class TeamPages(SubmissionTestCase):
    def setUp(self):
        super().setUp()
        self.upload()
        self.client.post(self.url("submit"), self.form(submit="1"))
        self.version = SubmissionVersion.objects.get()
        self.team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(self.team)
        self.changelist = reverse("admin:submissions_submissionversion_changelist")

    def act(self, action):
        return self.client.post(self.changelist, {"action": action, "_selected_action": [self.version.pk]})

    def test_the_manifest_export_is_valid_and_carries_the_teams_record(self):
        self.act("mark_received")
        self.act("mark_verified")
        response = self.act("export_manifest")
        data = json.loads(response.content)
        self.assertEqual(list(_validator("submission-manifest").iter_errors(data)), [])
        self.assertEqual((data["verification_status"], data["verified_by"]), ("verified", "team"))
        self.assertIn("received_at", data)
        self.assertEqual({"submission_received", "submission_verified", "manifest_exported"} -
                         set(EventLog.objects.values_list("operation", flat=True)), set())

    def test_records_cannot_be_edited_or_deleted_and_uploads_cannot_be_downloaded(self):
        upload = Upload.objects.get()
        for model, obj in (("upload", upload), ("submissionversion", self.version), ("submission", Submission.objects.get())):
            with self.subTest(model=model):
                self.assertEqual(self.client.post(reverse(f"admin:submissions_{model}_delete", args=[obj.pk]),
                                                  {"post": "yes"}).status_code, 403)
        page = self.client.get(reverse("admin:submissions_upload_change", args=[upload.pk]))
        self.assertContains(page, "code/run_all.do")                     # the listing of names and sizes
        self.assertNotContains(page, storage.path_of(upload).name)        # no link to the stored file

    def test_the_export_needs_permission_to_view_every_record(self):
        viewer = get_user_model().objects.create_user("viewer", "v@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.add(Permission.objects.get(codename="view_submissionversion"))
        self.client.force_login(viewer)
        self.assertNotIn("Content-Disposition", self.act("export_manifest"))

    def test_withdrawal_deletes_the_submission_and_the_files(self):
        path = storage.path_of(Upload.objects.get())
        self.assertTrue(path.is_file())
        self.client.post(reverse("admin:contributors_assignment_withdraw", args=[self.a_emp.pk]),
                         {"step": "3", "requested_on": timezone.localdate().isoformat(), "request_channel": "email",
                          "confirmation": self.a_emp.public_id})
        self.assertFalse(Assignment.objects.filter(pk=self.a_emp.pk).exists())
        self.assertFalse(path.exists())
        self.assertEqual((Upload.objects.count(), SubmissionVersion.objects.count(), Submission.objects.count()), (0, 0, 0))
        event = EventLog.objects.get(operation="withdrawn_on_request")
        self.assertEqual((event.details["uploads_deleted"], event.details["submission_versions_deleted"]), (1, 1))


class ReviewFindings(SubmissionTestCase):
    """Regression tests for the M3 review (2026-11-26) by Claude AI agents."""

    def damaged_zip(self):
        # A valid archive whose directory declares a ZIP version Python cannot read (NotImplementedError).
        data = bytearray(make_zip())
        at = data.rfind(b"PK\x01\x02")
        data[at + 6] = 0xCC
        return bytes(data)

    def test_an_archive_python_cannot_read_is_refused_never_stuck(self):
        body, _ = self.upload(data=self.damaged_zip())
        self.assertEqual(body["status"], "refused")
        self.assertFalse(Upload.objects.filter(status=Upload.CHECKING).exists())
        self.assertFalse(any((Path(self.private_root) / "uploads").rglob("*.part")))

    def test_a_check_that_never_finished_can_be_removed_or_run_again(self):
        started = self.start()[0].json()
        upload = Upload.objects.get(public_id=started["id"])
        data = make_zip()
        with open(storage.path_of(upload, part=True), "wb") as out:
            out.write(data)
        Upload.objects.filter(pk=upload.pk).update(received_bytes=len(data), status=Upload.CHECKING,
                                                   checking_since=timezone.now() - timezone.timedelta(hours=1))
        upload.refresh_from_db()
        self.assertTrue(storage.is_stale(upload))
        self.assertContains(self.client.get(self.url("submit")), "The check did not finish")
        done = storage.recheck(upload)                                   # the team's "Check again"
        self.assertEqual((done.status, done.sha256), (Upload.RECEIVED, hashlib.sha256(data).hexdigest()))

    def test_the_form_without_javascript_stores_privately_and_refuses_a_too_large_file(self):
        data = make_zip()
        self.client.post(self.url("upload_plain"), {"package": SimpleUploadedFile("pkg.zip", data)})
        self.assertEqual(Upload.objects.get().sha256, hashlib.sha256(data).hexdigest())
        incoming = Path(self.private_root) / "incoming"
        self.assertEqual(list(incoming.glob("*")) if incoming.exists() else [], [])       # moved, not left behind
        self.empirical.config["submission"] = {"accepted_channels": ["upload"], "max_upload_bytes": 50}
        self.empirical.save()
        page = self.client.post(self.url("upload_plain"), {"package": SimpleUploadedFile("big.zip", data)}, follow=True)
        self.assertContains(page, "larger than")
        self.assertEqual(Upload.objects.count(), 1)

    def test_the_plain_form_still_checks_csrf(self):
        client = self.client_class(enforce_csrf_checks=True)
        client.cookies = self.client.cookies
        response = client.post(self.url("upload_plain"), {"package": SimpleUploadedFile("pkg.zip", make_zip())})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Upload.objects.exists())

    def test_byte_budget_and_free_space(self):
        self.empirical.config["submission"] = {"accepted_channels": ["upload"], "max_upload_bytes": 1000}
        self.empirical.save()
        with override_settings(UPLOAD_BUDGET_FACTOR=2):
            self.start(name="a.zip", size=900, data=b"x" * 900)
            self.start(name="b.zip", size=900, data=b"y" * 900)
            third = self.start(name="c.zip", size=900, data=b"z" * 900)[0]
        self.assertEqual(third.json()["error"], "over_budget")
        from collections import namedtuple
        usage = namedtuple("usage", "total used free")(10 ** 12, 10 ** 12, 10)
        with mock.patch("submissions.storage.shutil.disk_usage", return_value=usage):
            self.assertEqual(self.start(name="d.zip", size=10, data=b"w" * 10)[0].json()["error"], "disk_full")

    def test_unfinished_uploads_expire(self):
        started = self.start()[0].json()
        Upload.objects.filter(public_id=started["id"]).update(updated_at=timezone.now() - timezone.timedelta(days=31))
        out = io.StringIO()
        call_command("expire_uploads", stdout=out)
        self.assertIn("Deleted 1", out.getvalue())
        self.assertFalse(Upload.objects.exists())
        self.assertFalse(any((Path(self.private_root) / "uploads").rglob("*.part")))

    def test_a_replaced_archive_can_be_left_out_of_later_versions(self):
        first, _ = self.upload(name="first.zip")
        self.client.post(self.url("submit"), self.form(submit="1"))
        second, _ = self.upload(data=make_zip({"README.md": "corrected"}), name="second.zip")
        self.client.post(self.url("upload_include", first["id"]), {"include": "0"})
        self.client.post(self.url("submit"), self.form(submit="1"))
        v1, v2 = SubmissionVersion.objects.order_by("version")
        self.assertEqual([f["path"] for f in v1.manifest["files"]], ["first.zip"])
        self.assertEqual([f["path"] for f in v2.manifest["files"]], ["second.zip"])

    def test_the_ai_disclosure_covers_what_the_contributor_writes_here(self):
        self.upload()
        page = self.client.post(self.url("submit"), self.form(submit="1", ai_used="on"))
        self.assertContains(page, "Please name the tool.")
        self.client.post(self.url("submit"), self.form(submit="1", ai_used="on", ai_tool="a chat assistant",
                                                       ai_account_kind="work"))
        help_ = SubmissionVersion.objects.get().manifest["ai_help"]
        self.assertEqual((help_["used"], help_["tool"], help_["entered_items_or_package"]), (True, "a chat assistant", False))

    def test_not_decided_data_another_channel_and_form_rules(self):
        self.client.post(self.url("submit"), self.form(
            submit="1", channel="other_agreed", other_channel_note="Institutional transfer agreed by e-mail",
            software="Stata，18", **{"datasets-0-availability": "not_decided", "datasets-0-access_route": ""}))
        version = SubmissionVersion.objects.get()
        self.assertEqual(version.manifest["other_channel_note"], "Institutional transfer agreed by e-mail")
        self.assertEqual(version.manifest["datasets"][0]["availability"], "not_decided")
        self.assertEqual(version.manifest["package"]["software"], [{"name": "Stata", "version": "18"}])
        page = self.client.post(self.url("submit"), self.form(save="1", version="1", status_qualifications="",
                                                              note_qualifications="a limitation"))
        self.assertContains(page, "Choose a status for this note.")

    def test_removing_a_dataset_survives_a_validation_error(self):
        self.client.post(self.url("submit"), self.form(save="1"))
        page = self.client.post(self.url("submit"), self.form(
            save="1", version="1", software="no comma", **{"datasets-INITIAL_FORMS": "1", "datasets-0-DELETE": "on"}))
        self.assertContains(page, "Write each line as name, version")
        self.assertContains(page, 'name="datasets-0-DELETE"')

    def test_submitting_twice_from_one_page_creates_one_version(self):
        self.upload()
        form = self.form(submit="1")
        self.client.post(self.url("submit"), form)
        second = self.client.post(self.url("submit"), form, follow=True)        # the same page, pressed again
        self.assertContains(second, "saved from another tab")
        self.assertEqual(SubmissionVersion.objects.count(), 1)

    def test_an_unfinished_upload_does_not_block_a_paper_that_no_longer_takes_uploads(self):
        started = self.start()[0].json()
        self.empirical.config["submission"] = {"accepted_channels": ["public_reference"]}
        self.empirical.save()
        self.client.post(self.url("submit"), self.form(submit="1", channel="public_reference", pub_repository="r",
                                                       pub_identifier="i", pub_version="v"))
        self.assertEqual(SubmissionVersion.objects.count(), 1)
        self.client.post(self.url("upload_remove", started["id"]))                # and it can still be removed
        self.assertFalse(Upload.objects.exists())
        self.assertEqual(self.client.get(self.url("upload_status", started["id"])).status_code, 404)

    def test_withdrawal_deletes_unfinished_and_refused_uploads_too(self):
        unfinished = self.start(name="half.zip")[0].json()
        self.chunk(unfinished["id"], 0, b"PK")
        self.upload(data=b"not a zip", name="bad.zip")
        team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(team)
        self.client.post(reverse("admin:contributors_assignment_withdraw", args=[self.a_emp.pk]),
                         {"step": "3", "requested_on": timezone.localdate().isoformat(), "request_channel": "email",
                          "confirmation": self.a_emp.public_id})
        self.assertFalse(Upload.objects.exists())
        self.assertEqual(list((Path(self.private_root) / "uploads").rglob("*.*")), [])

    def test_remove_needs_a_second_step_and_names_the_file(self):
        self.upload(name="named.zip")
        page = self.client.get(self.url("submit")).content.decode()
        self.assertIn('<details class="confirm-remove">', page)
        self.assertIn("Delete named.zip from the site", page)
