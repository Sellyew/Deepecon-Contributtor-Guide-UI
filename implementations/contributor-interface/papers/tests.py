"""Importer and administration tests (plan §2.1; M1 runs with fictional examples only)."""
import hashlib
import io
import json
import tempfile
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import CommandError, call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from deepecon_site.testing import PrivateStorageMixin, example_bytes, example_json, import_example
from papers import importers
from papers.models import CandidatePackage, EventLog, ExposureLogEntry, Item, ItemMap, Paper, RubricVersion


def evaluation_run(paper, **extra):
    return ExposureLogEntry.objects.create(paper=paper, occurred_on=date(2026, 12, 1), ai_service="example API",
                                           developer="Example Labs", material="package_and_trajectory",
                                           route="evaluation_run", account_kind="api", recorded_by="test",
                                           model_version="example-model-2026-10-01", model_release_date=date(2026, 10, 1),
                                           **extra)


def synthetic(paper_id):
    from contributors.management.commands.load_demo import synthetic_package
    return synthetic_package(paper_id)


class ImporterTests(PrivateStorageMixin, TestCase):
    def test_both_fields_import_with_their_own_categories(self):
        empirical = import_example("empirical")
        theory = import_example("theory")
        self.assertEqual(set(empirical.current_rubric().items.values_list("category", flat=True)),
                         {"conceptual", "missing", "technical"})
        self.assertEqual(set(theory.current_rubric().items.values_list("category", flat=True)),
                         {"derivation", "assumption", "proof-gap"})

    def test_publication_status_is_imported(self):
        self.assertEqual(import_example("empirical").publication_status, Paper.SCORED)
        theory = import_example("theory")
        self.assertEqual(theory.publication_status, Paper.DEMO)
        self.assertEqual(theory.designated_on, date(2026, 11, 7))

    def test_invalid_configuration_is_refused(self):
        config = example_json("empirical", "paper-config")
        del config["citation"]
        with self.assertRaises(importers.ImportRefused):
            importers.import_paper_config(json.dumps(config).encode(), "test")
        self.assertFalse(Paper.objects.exists())

    def test_rubric_failing_a_check_is_refused(self):
        paper = importers.import_paper_config(example_bytes("empirical", "paper-config"), "test")
        rubric = example_json("empirical", "rubric")
        rubric["conceptual"][0]["points"] += 1
        with self.assertRaises(importers.ImportRefused) as refused:
            importers.import_rubric(paper, json.dumps(rubric).encode(), "test")
        self.assertTrue(any("largest allowed score" in p for p in refused.exception.problems))
        self.assertFalse(RubricVersion.objects.exists())

    def test_item_map_with_unknown_anchor_is_refused(self):
        paper = importers.import_paper_config(example_bytes("empirical", "paper-config"), "test")
        importers.import_rubric(paper, example_bytes("empirical", "rubric"), "test")
        item_map = example_json("empirical", "item-map")
        first = next(iter(item_map["items"]))
        item_map["items"][first]["anchors"] = ["nowhere"]
        with self.assertRaises(importers.ImportRefused):
            importers.import_item_map(paper, json.dumps(item_map).encode(), "test")
        self.assertFalse(ItemMap.objects.exists())

    def test_item_map_needs_its_rubric(self):
        paper = importers.import_paper_config(example_bytes("empirical", "paper-config"), "test")
        with self.assertRaises(importers.ImportRefused):
            importers.import_item_map(paper, example_bytes("empirical", "item-map"), "test")

    def test_item_origin_is_stored(self):
        paper = import_example("empirical")
        origins = [i.origin for i in paper.current_rubric().items.all() if i.origin]
        self.assertTrue(any(o["drafted_by"] == "ai_service" and o["model_family"] for o in origins))

    def test_package_with_wrong_hash_is_refused_and_not_stored(self):
        config = example_json("empirical", "paper-config")
        config["candidate_package_sha256"] = hashlib.sha256(b"something else").hexdigest()
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        from contributors.management.commands.load_demo import synthetic_package
        with self.assertRaises(importers.ImportRefused):
            importers.import_candidate_package(paper, io.BytesIO(synthetic_package(paper.paper_id)), "test")
        self.assertFalse(CandidatePackage.objects.exists())
        self.assertEqual([p for p in Path(self.private_root).rglob("*") if p.is_file()], [])

    def test_package_must_be_a_zip(self):
        config = example_json("empirical", "paper-config")
        config["candidate_package_sha256"] = hashlib.sha256(b"not a zip").hexdigest()
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        with self.assertRaises(importers.ImportRefused) as refused:
            importers.import_candidate_package(paper, io.BytesIO(b"not a zip"), "test")
        self.assertTrue(any("not a ZIP" in p for p in refused.exception.problems))

    def test_package_is_kept_in_private_storage(self):
        paper = import_example("empirical")
        path = importers.package_path(paper.current_package())
        self.assertTrue(path.is_file())
        self.assertTrue(str(path).startswith(self.private_root))
        for static_dir in settings.STATICFILES_DIRS:
            self.assertFalse(str(path).startswith(str(static_dir)))

    def test_event_log_holds_no_item_text(self):
        paper = import_example("empirical")
        texts = [i.normalized["title"] for i in paper.current_rubric().items.all() if i.normalized.get("title")]
        logged = json.dumps([e.details for e in EventLog.objects.all()], ensure_ascii=False)
        self.assertTrue(texts)
        for text in texts:
            self.assertNotIn(text, logged)

    def test_scored_task_with_evaluation_runs_cannot_become_demo(self):
        paper = import_example("empirical")
        ExposureLogEntry.objects.create(paper=paper, occurred_on=date(2026, 12, 1), ai_service="example API",
                                        developer="Example Labs", material="package_and_trajectory",
                                        route="evaluation_run", account_kind="api", recorded_by="test")
        config = dict(paper.config, publication_status={"status": "demo_or_development", "designated_on": "2026-12-02"})
        with self.assertRaises(importers.ImportRefused):
            importers.import_paper_config(json.dumps(config).encode(), "test")
        paper.refresh_from_db()
        self.assertEqual(paper.publication_status, Paper.SCORED)

    # Candidate packages (plan §2.1).

    def test_package_without_a_configured_hash_is_refused(self):
        config = example_json("empirical", "paper-config")
        config.pop("candidate_package_sha256", None)
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        with self.assertRaises(importers.ImportRefused) as refused:
            importers.import_candidate_package(paper, io.BytesIO(synthetic(paper.paper_id)), "test")
        self.assertTrue(any("no candidate_package_sha256" in p for p in refused.exception.problems))
        self.assertFalse(CandidatePackage.objects.exists())
        self.assertEqual([p for p in Path(self.private_root).rglob("*") if p.is_file()], [])

    def test_candidate_version_cannot_leave_private_storage(self):
        package = synthetic("example-school-leadership")
        config = example_json("empirical", "paper-config")
        config["candidate_package_sha256"] = hashlib.sha256(package).hexdigest()
        config["candidate_version"] = "../../../../outside"
        with self.assertRaises(importers.ImportRefused):
            importers.import_paper_config(json.dumps(config).encode(), "test")      # the schema refuses it
        del config["candidate_version"]
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        for version in ("../../../../outside", "/tmp/absolute", "a/b"):
            with self.assertRaises(importers.ImportRefused):
                importers.import_candidate_package(paper, io.BytesIO(package), "test", candidate_version=version)
        self.assertFalse(CandidatePackage.objects.exists())
        self.assertFalse((Path(self.private_root).parent / f"outside-{config['candidate_package_sha256'][:12]}.zip").exists())

    def test_unversioned_package_is_current(self):
        package = synthetic("example-school-leadership")
        config = example_json("empirical", "paper-config")
        config["candidate_package_sha256"] = hashlib.sha256(package).hexdigest()
        config.pop("candidate_version", None)
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        importers.import_candidate_package(paper, io.BytesIO(package), "test")
        self.assertEqual(paper.current_package().candidate_version, "unversioned")

    def test_only_the_package_named_by_the_current_hash_is_current(self):
        paper = import_example("empirical")
        self.assertIsNotNone(paper.current_package())
        config = dict(paper.config, candidate_package_sha256=hashlib.sha256(b"a newer package").hexdigest())
        paper = importers.import_paper_config(json.dumps(config).encode(), "test")
        self.assertIsNone(paper.current_package())

    # Rubric re-imports keep provenance (Rule 7) and stored files (plan §2.1).

    def test_reimporting_the_same_rubric_keeps_items_and_origins(self):
        paper = import_example("empirical")
        before = list(Item.objects.order_by("pk").values_list("pk", "origin"))
        importers.import_rubric(paper, example_bytes("empirical", "rubric"), "test")
        self.assertEqual(list(Item.objects.order_by("pk").values_list("pk", "origin")), before)

    def test_changed_rubric_under_the_same_version_is_refused(self):
        paper = import_example("empirical")
        rubric = example_json("empirical", "rubric")
        rubric["conceptual"][0][paper.config["categories"][0]["field_roles"]["title"]] = "A different title"
        with self.assertRaises(importers.ImportRefused):
            importers.import_rubric(paper, json.dumps(rubric).encode(), "test")
        self.assertEqual(paper.current_rubric().sha256, hashlib.sha256(example_bytes("empirical", "rubric")).hexdigest())

    # Rubric checks refuse malformed files instead of failing (validation/rubric_checks.py).

    def _refused_rubric(self, change):
        paper = importers.import_paper_config(example_bytes("empirical", "paper-config"), "test")
        rubric = example_json("empirical", "rubric")
        change(rubric)
        with self.assertRaises(importers.ImportRefused) as refused:
            importers.import_rubric(paper, json.dumps(rubric).encode(), "test")
        self.assertFalse(RubricVersion.objects.exists())
        return refused.exception.problems

    def test_points_must_be_numbers(self):
        for value in (None, "5", True):
            problems = self._refused_rubric(lambda r: r["conceptual"][0].__setitem__("points", value))
            self.assertTrue(any("not a number" in p for p in problems), value)

    def test_item_entries_must_be_objects_with_valid_ids(self):
        self._refused_rubric(lambda r: r["conceptual"].append("not an object"))
        for bad in ("conceptual error number 1", 7, "a b"):
            problems = self._refused_rubric(lambda r: r["conceptual"][0].__setitem__("id", bad))
            self.assertTrue(any("must be 1-16" in p for p in problems), bad)

    # Configuration re-imports (plan §2.1; Rule 8).

    def test_duplicate_category_ids_are_refused(self):
        config = example_json("empirical", "paper-config")
        config["categories"][1]["id"] = config["categories"][0]["id"]
        with self.assertRaises(importers.ImportRefused) as refused:
            importers.import_paper_config(json.dumps(config).encode(), "test")
        self.assertTrue(any("duplicate" in p for p in refused.exception.problems))

    def test_config_reimport_renormalizes_the_stored_rubric(self):
        paper = import_example("theory")
        config = json.loads(json.dumps(paper.config))
        old = config["categories"][0]["id"]
        config["categories"][0]["id"] = "derivation-step"
        importers.import_paper_config(json.dumps(config).encode(), "test")
        categories = set(paper.current_rubric().items.values_list("category", flat=True))
        self.assertIn("derivation-step", categories)
        self.assertNotIn(old, categories)

    def test_config_reimport_that_no_longer_fits_the_rubric_is_refused(self):
        paper = import_example("theory")
        config = json.loads(json.dumps(paper.config))
        config["categories"][0]["source_array"] = "no_such_array"
        with self.assertRaises(importers.ImportRefused):
            importers.import_paper_config(json.dumps(config).encode(), "test")
        paper.refresh_from_db()
        self.assertNotEqual(paper.config["categories"][0]["source_array"], "no_such_array")

    def test_designation_is_fixed_after_an_evaluation_run(self):
        theory = import_example("theory")                         # demo, designated 2026-11-07
        evaluation_run(theory)
        changes = [{"status": "scored"},
                   {"status": "demo_or_development", "designated_on": "2026-12-02"},
                   None]                                         # omitting the status means scored
        for status in changes:
            config = {k: v for k, v in theory.config.items() if k != "publication_status"}
            if status:
                config["publication_status"] = status
            with self.assertRaises(importers.ImportRefused, msg=status):
                importers.import_paper_config(json.dumps(config).encode(), "test")
        theory.refresh_from_db()
        self.assertEqual((theory.publication_status, theory.designated_on), (Paper.DEMO, date(2026, 11, 7)))
        importers.import_paper_config(json.dumps(theory.config).encode(), "test")   # an unchanged designation is fine

    def test_evaluation_runs_need_the_model_version_and_release_date(self):
        paper = import_example("empirical")
        entry = ExposureLogEntry(paper=paper, occurred_on=date(2026, 12, 1), ai_service="example API",
                                 developer="Example Labs", material="package_and_trajectory",
                                 route="evaluation_run", account_kind="api", recorded_by="test")
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_event_log_names_papers_by_their_id(self):
        paper = import_example("empirical")
        rubric_event = EventLog.objects.get(operation="import_rubric")
        self.assertTrue(rubric_event.object_id.startswith(paper.paper_id + " "))

    def test_import_commands(self):
        examples = Path(settings.SCHEMA_DIR) / "examples" / "theory"
        call_command("import_paper_config", str(examples / "paper-config.json"), stdout=io.StringIO())
        call_command("import_rubric", "example-matching-theory", str(examples / "rubric.json"), stdout=io.StringIO())
        call_command("import_item_map", "example-matching-theory", str(examples / "item-map.json"), stdout=io.StringIO())
        self.assertTrue(ItemMap.objects.filter(paper__paper_id="example-matching-theory").exists())
        bad = example_json("theory", "rubric")
        bad["version"] = "another_version"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(bad, handle)
        with self.assertRaises(CommandError):
            call_command("import_rubric", "example-matching-theory", handle.name, stdout=io.StringIO(), stderr=io.StringIO())


class AdminImportTests(PrivateStorageMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(self.admin)

    def test_import_page_imports_a_configuration(self):
        upload = SimpleUploadedFile("paper-config.json", example_bytes("theory", "paper-config"), content_type="application/json")
        response = self.client.post(reverse("admin:papers_import"), {"kind": "paper_config", "file": upload})
        self.assertRedirects(response, reverse("admin:papers_paper_changelist"))
        self.assertTrue(Paper.objects.filter(paper_id="example-matching-theory").exists())

    def test_import_page_shows_problems_and_stores_nothing(self):
        config = example_json("theory", "paper-config")
        del config["categories"]
        upload = SimpleUploadedFile("paper-config.json", json.dumps(config).encode(), content_type="application/json")
        response = self.client.post(reverse("admin:papers_import"), {"kind": "paper_config", "file": upload})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fails the")
        self.assertFalse(Paper.objects.exists())


class AdminPermissionTests(PrivateStorageMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.paper = import_example("empirical")
        self.viewer = get_user_model().objects.create_user("viewer", "viewer@example.org", "a-long-test-password", is_staff=True)
        self.viewer.user_permissions.set(Permission.objects.filter(codename__startswith="view_"))

    def test_view_only_staff_cannot_import(self):
        self.client.force_login(self.viewer)
        config = dict(self.paper.config, citation=dict(self.paper.config["citation"], title="Overwritten"))
        upload = SimpleUploadedFile("paper-config.json", json.dumps(config).encode(), content_type="application/json")
        with self.assertLogs("django.request", level="WARNING"):
            response = self.client.post(reverse("admin:papers_import"), {"kind": "paper_config", "file": upload})
        self.assertEqual(response.status_code, 403)
        self.paper.refresh_from_db()
        self.assertNotEqual(self.paper.title, "Overwritten")

    def test_exposure_log_is_append_only(self):
        team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(team)
        response = self.client.post(reverse("admin:papers_exposurelogentry_add"), {
            "paper": self.paper.pk, "occurred_on": "2026-11-07", "ai_service": "example assistant",
            "developer": "Example Labs", "api_host": "", "material": "answer_key", "route": "construction",
            "account_kind": "work", "model_version": "", "model_release_date": "", "notes": "",
            "recorded_by": "someone else"})
        self.assertEqual(response.status_code, 302)
        entry = ExposureLogEntry.objects.get()
        self.assertEqual(entry.recorded_by, "team")
        self.assertTrue(EventLog.objects.filter(operation="exposure_recorded", details__exposure_id=entry.pk).exists())
        change_url = reverse("admin:papers_exposurelogentry_change", args=[entry.pk])
        with self.assertLogs("django.request", level="WARNING"):
            response = self.client.post(change_url, {"paper": self.paper.pk, "occurred_on": "2027-06-01", "ai_service": "x",
                                                     "developer": "Other Labs", "material": "answer_key",
                                                     "route": "calibration", "account_kind": "work"})
        self.assertEqual(response.status_code, 403)
        entry.refresh_from_db()
        self.assertEqual((entry.occurred_on, entry.developer, entry.route), (date(2026, 11, 7), "Example Labs", "construction"))


class RunserverTests(SimpleTestCase):
    def test_stage_0_refuses_non_loopback_addresses(self):
        for address in ("0.0.0.0:8000", "0:8000", "192.168.1.5:8000", "[::]:8000"):
            with self.assertRaises(CommandError):
                call_command("runserver", address, use_reloader=False)
