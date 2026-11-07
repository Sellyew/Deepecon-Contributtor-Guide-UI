"""Importer and administration tests (plan §2.1; M1 runs with fictional examples only)."""
import hashlib
import io
import json
import tempfile
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import CommandError, call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from deepecon_site.testing import PrivateStorageMixin, example_bytes, example_json, import_example
from papers import importers
from papers.models import CandidatePackage, EventLog, ExposureLogEntry, ItemMap, Paper, RubricVersion


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


class RunserverTests(SimpleTestCase):
    def test_stage_0_refuses_non_loopback_addresses(self):
        for address in ("0.0.0.0:8000", "0:8000", "192.168.1.5:8000", "[::]:8000"):
            with self.assertRaises(CommandError):
                call_command("runserver", address, use_reloader=False)
