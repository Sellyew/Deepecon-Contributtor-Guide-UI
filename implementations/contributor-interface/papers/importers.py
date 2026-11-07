"""Importers for the team's files (plan §2.1).

Each importer validates its file against the contributor-interface JSON Schemas and the
consistency checks in validation/rubric_checks.py, and refuses the import if anything fails.
Files are stored as they are. Problem messages name fields and IDs; the event log records
only IDs, counts, and hashes.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
import zipfile
from datetime import date
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.db import transaction
from jsonschema import Draft202012Validator, FormatChecker

from .models import CandidatePackage, Item, ItemMap, Paper, RubricVersion, log_event


class ImportRefused(Exception):
    def __init__(self, problems):
        self.problems = list(problems)
        super().__init__("; ".join(self.problems))


@lru_cache(maxsize=1)
def rubric_checks():
    """validation/rubric_checks.py from the repository (standard library only)."""
    path = Path(settings.VALIDATION_DIR) / "rubric_checks.py"
    spec = importlib.util.spec_from_file_location("rubric_checks", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def _validator(name):
    schema = json.loads((Path(settings.SCHEMA_DIR) / f"{name}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _validate(name, data):
    errors = sorted(_validator(name).iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        problems = []
        for e in errors[:25]:
            where = "/".join(str(p) for p in e.absolute_path) or "(top level)"
            problems.append(f"{name}: {where}: fails the '{e.validator}' rule")
        raise ImportRefused(problems)


def _load(content):
    if isinstance(content, (str, os.PathLike)):
        content = Path(content).read_bytes()
    sha = hashlib.sha256(content).hexdigest()
    try:
        data = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ImportRefused([f"not valid UTF-8 JSON ({type(exc).__name__})"])
    return data, sha


@transaction.atomic
def import_paper_config(content, actor):
    data, sha = _load(content)
    _validate("paper-config", data)
    status = data.get("publication_status", {"status": Paper.SCORED})
    existing = Paper.objects.filter(paper_id=data["paper_id"]).first()
    if (existing and existing.publication_status == Paper.SCORED and status["status"] == Paper.DEMO
            and existing.exposures.filter(route="evaluation_run").exists()):
        # Rule 8: a scored task is not redesignated after any evaluation run.
        raise ImportRefused([f"{data['paper_id']}: a scored task with evaluation runs cannot be redesignated as demo or development"])
    designated = status.get("designated_on")
    paper, created = Paper.objects.update_or_create(
        paper_id=data["paper_id"],
        defaults={
            "field": data.get("field", ""),
            "title": data["citation"]["title"],
            "config": data,
            "config_sha256": sha,
            "publication_status": status["status"],
            "designated_on": date.fromisoformat(designated) if designated else None,
        },
    )
    log_event(actor, "import_paper_config", paper, sha256=sha, created=created,
              categories=[c["id"] for c in data["categories"]], publication_status=status["status"])
    return paper


@transaction.atomic
def import_rubric(paper, content, actor):
    data, sha = _load(content)
    _validate("rubric-import", data)
    rc = rubric_checks()
    items, _ = rc.normalize(data, paper.config)
    problems = rc.check_rubric(data, paper.config)          # includes the normalization problems
    if problems:
        raise ImportRefused(problems)
    rubric, _ = RubricVersion.objects.update_or_create(
        paper=paper, version=data["version"], defaults={"raw": data, "sha256": sha}
    )
    rubric.items.all().delete()
    Item.objects.bulk_create([
        Item(rubric=rubric, item_id=it["id"], category=it["category"], position=i,
             normalized={k: v for k, v in it.items() if k != "raw"})
        for i, it in enumerate(items)
    ])
    counts = {}
    for it in items:
        counts[it["category"]] = counts.get(it["category"], 0) + 1
    log_event(actor, "import_rubric", rubric, sha256=sha, items_per_category=counts)
    return rubric


@transaction.atomic
def import_item_map(paper, content, actor):
    data, sha = _load(content)
    _validate("item-map", data)
    problems = []
    if data["paper_id"] != paper.paper_id:
        problems.append(f"item map is for paper {data['paper_id']}, not {paper.paper_id}")
    rubric = paper.rubrics.filter(version=data["rubric_version"]).first()
    if rubric is None:
        raise ImportRefused(problems + [f"rubric version {data['rubric_version']} has not been imported for {paper.paper_id}"])
    items = list(rubric.items.order_by("position"))
    problems += rubric_checks().check_item_map(data, [it.normalized for it in items])
    if problems:
        raise ImportRefused(problems)
    item_map, _ = ItemMap.objects.update_or_create(paper=paper, rubric=rubric, defaults={"raw": data, "sha256": sha})
    for it in items:
        it.origin = data["items"].get(it.item_id, {}).get("origin")
        it.save(update_fields=["origin"])
    log_event(actor, "import_item_map", item_map, sha256=sha, nodes=len(data["nodes"]), items=len(data["items"]))
    return item_map


def import_candidate_package(paper, source, actor, candidate_version=None):
    """Stores the agent-facing ZIP in private storage after checking its SHA-256.

    `source` is a path or a binary file object. Nothing in the package is executed; it is
    opened only to confirm that it is a ZIP archive.
    """
    root = Path(settings.PRIVATE_STORAGE_ROOT)
    incoming = root / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    size = 0
    fd, tmp = tempfile.mkstemp(dir=incoming, suffix=".zip")
    try:
        with os.fdopen(fd, "wb") as out:
            stream = open(source, "rb") if isinstance(source, (str, os.PathLike)) else source
            try:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
                    size += len(chunk)
                    out.write(chunk)
            finally:
                if stream is not source:
                    stream.close()
        sha = digest.hexdigest()
        expected = paper.config.get("candidate_package_sha256")
        problems = []
        if expected and expected != sha:
            problems.append("the package's SHA-256 differs from candidate_package_sha256 in the paper configuration")
        if not zipfile.is_zipfile(tmp):
            problems.append("the package is not a ZIP archive")
        if problems:
            raise ImportRefused(problems)
        version = candidate_version or paper.config.get("candidate_version") or "unversioned"
        rel = Path("papers") / paper.paper_id / "candidate" / f"{version}-{sha[:12]}.zip"
        final = root / rel
        final.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp, final)
        tmp = None
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    with transaction.atomic():
        package, _ = CandidatePackage.objects.update_or_create(
            paper=paper, candidate_version=version,
            defaults={"sha256": sha, "size_bytes": size, "storage_name": str(rel)},
        )
        log_event(actor, "import_candidate_package", package, sha256=sha, size_bytes=size)
    return package


def package_path(package):
    return Path(settings.PRIVATE_STORAGE_ROOT) / package.storage_name
