from django.core.management.base import BaseCommand

from papers import importers

from ._base import actor, run


class Command(BaseCommand):
    help = "Validate and import a paper configuration (paper-config.json)."

    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, **options):
        run(self, importers.import_paper_config, path, actor())
