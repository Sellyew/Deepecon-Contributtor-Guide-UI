"""Shared helpers for the import commands."""
import getpass

from django.core.management.base import CommandError

from papers import importers
from papers.models import Paper


def actor():
    return f"cli:{getpass.getuser()}"


def paper_or_fail(paper_id):
    paper = Paper.objects.filter(paper_id=paper_id).first()
    if paper is None:
        raise CommandError(f"Paper {paper_id} has no imported configuration; run import_paper_config first.")
    return paper


def run(command, fn, *args):
    try:
        result = fn(*args)
    except importers.ImportRefused as refused:
        for problem in refused.problems:
            command.stderr.write(f"  - {problem}")
        raise CommandError("Import refused; nothing was stored.")
    command.stdout.write(command.style.SUCCESS(f"Imported {result}."))
    return result
