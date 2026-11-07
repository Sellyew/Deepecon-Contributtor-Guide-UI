"""Shared test helpers: a temporary private storage root and the fictional examples."""
import hashlib
import io
import json
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.test import override_settings

EXAMPLES = Path(settings.SCHEMA_DIR) / "examples"


def example_bytes(field, name):
    return (EXAMPLES / field / f"{name}.json").read_bytes()


def example_json(field, name):
    return json.loads(example_bytes(field, name))


class PrivateStorageMixin:
    """Each test gets its own private storage directory."""

    def setUp(self):
        super().setUp()
        self.private_root = tempfile.mkdtemp(prefix="deepecon-test-")
        self._storage = override_settings(PRIVATE_STORAGE_ROOT=self.private_root)
        self._storage.enable()

    def tearDown(self):
        self._storage.disable()
        shutil.rmtree(self.private_root, ignore_errors=True)
        super().tearDown()


def import_example(field, actor="test"):
    """Import one fictional example with a synthetic package; returns the Paper."""
    from contributors.management.commands.load_demo import synthetic_package
    from papers import importers

    config = example_json(field, "paper-config")
    package = synthetic_package(config["paper_id"])
    config["candidate_package_sha256"] = hashlib.sha256(package).hexdigest()
    paper = importers.import_paper_config(json.dumps(config).encode("utf-8"), actor)
    importers.import_rubric(paper, example_bytes(field, "rubric"), actor)
    importers.import_item_map(paper, example_bytes(field, "item-map"), actor)
    importers.import_candidate_package(paper, io.BytesIO(package), actor)
    return paper
