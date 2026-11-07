from django.core.management.base import BaseCommand

from papers import importers

from ._base import actor, paper_or_fail, run


class Command(BaseCommand):
    help = "Store the agent-facing candidate ZIP in private storage after checking its SHA-256 against the configuration."

    def add_arguments(self, parser):
        parser.add_argument("paper_id")
        parser.add_argument("path")
        parser.add_argument("--candidate-version", default=None)

    def handle(self, paper_id, path, candidate_version=None, **options):
        paper = paper_or_fail(paper_id)
        run(self, lambda: importers.import_candidate_package(paper, path, actor(), candidate_version))
