"""Re-run every import check on every stored paper (D-049).

Rules change; papers imported under an older rule are not re-checked by themselves. This
command applies today's checks to everything stored and fails if any paper has a problem.
"""
import hashlib

from django.core.management.base import BaseCommand, CommandError

from papers import importers
from papers.models import Paper


def paper_problems(paper):
    """Every check the importers make, applied to what is stored, plus the stored items and package."""
    problems = importers.config_problems(paper.config)
    if problems:
        return problems                     # the other checks read the configuration
    rc = importers.rubric_checks()
    rubric = paper.current_rubric()
    if rubric is None:
        problems.append(f"rubric version {paper.config.get('rubric_version')} is not imported")
    else:
        problems += importers.rubric_problems(rubric.raw, paper.config)
        if not problems:
            items, _ = rc.normalize(rubric.raw, paper.config)
            stored = set(rubric.items.values_list("item_id", flat=True))
            if {it["id"] for it in items} != stored:
                problems.append(f"the categories select different items from the stored rubric {rubric.version}")
        item_map = rubric.item_maps.first()
        if item_map is None:
            problems.append("no item map is imported for the current rubric")
        else:
            problems += importers.item_map_problems(item_map.raw, paper, rubric)
        missing = list(rubric.items.filter(origin__isnull=True).values_list("item_id", flat=True))
        if missing:
            problems.append(f"items without provenance: {', '.join(missing)}")
    expected = paper.config.get("candidate_package_sha256")
    package = paper.current_package()
    if expected and package is None:
        problems.append("the configured candidate package is not imported")
    elif package is not None:
        path = importers.package_path(package)
        if not path.is_file():
            problems.append(f"the candidate package file is missing: {package.storage_name}")
        else:
            digest = hashlib.sha256()
            with open(path, "rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != package.sha256:
                problems.append("the stored candidate package no longer matches its SHA-256")
    if paper.built_on is None:
        problems.append("no task build date (Rule 10); needed before freezing a review")
    return problems


class Command(BaseCommand):
    help = "Apply today's import checks to every stored paper; fails if any paper has a problem."

    def handle(self, **options):
        failing = 0
        for paper in Paper.objects.all():
            problems = paper_problems(paper)
            if problems:
                failing += 1
                self.stdout.write(f"{paper.paper_id}: {len(problems)} problem(s)")
                for problem in problems:
                    self.stdout.write(f"  - {problem}")
            else:
                self.stdout.write(f"{paper.paper_id}: ok")
        if failing:
            raise CommandError(f"{failing} paper(s) need attention.")
