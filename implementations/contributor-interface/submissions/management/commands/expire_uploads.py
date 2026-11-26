"""Delete unfinished uploads left untouched for a number of days (default UPLOAD_UNFINISHED_DAYS).

The Submit page tells contributors how long an unfinished upload is kept. Run this daily on the
server (M6); at Stage 0, run it by hand.
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from submissions.storage import expire_unfinished


class Command(BaseCommand):
    help = "Delete unfinished uploads untouched for N days (default: UPLOAD_UNFINISHED_DAYS)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=settings.UPLOAD_UNFINISHED_DAYS)

    def handle(self, days, **options):
        self.stdout.write(f"Deleted {expire_unfinished(days)} unfinished upload(s) untouched for {days} days.")
