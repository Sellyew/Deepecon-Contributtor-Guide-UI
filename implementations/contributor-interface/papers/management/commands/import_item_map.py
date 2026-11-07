from django.core.management.base import BaseCommand

from papers import importers

from ._base import actor, paper_or_fail, run


class Command(BaseCommand):
    help = "Validate the item map (nodes, edges, anchors, excerpts) against the imported rubric and import it."

    def add_arguments(self, parser):
        parser.add_argument("paper_id")
        parser.add_argument("path")

    def handle(self, paper_id, path, **options):
        run(self, importers.import_item_map, paper_or_fail(paper_id), path, actor())
