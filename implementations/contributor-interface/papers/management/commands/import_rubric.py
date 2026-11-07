from django.core.management.base import BaseCommand

from papers import importers

from ._base import actor, paper_or_fail, run


class Command(BaseCommand):
    help = "Store the team's rubric file as it is and normalize it through the paper's categories; refused if any check fails."

    def add_arguments(self, parser):
        parser.add_argument("paper_id")
        parser.add_argument("path")

    def handle(self, paper_id, path, **options):
        run(self, importers.import_rubric, paper_or_fail(paper_id), path, actor())
