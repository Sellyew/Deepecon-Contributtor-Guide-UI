"""Create the unpublished tripwire GUID (D-049, docs/methodology/canary.md).

Run this on a team computer. The GUID is written to the private data folder and never
printed, so it does not pass through a terminal transcript or an AI assistant's session.
Team tooling that builds evaluation internals reads it with tripwire_path().

Replacing it keeps the old one: evaluation internals built before the replacement still carry
the old GUID, so probes for leaks must look for every retired GUID too (retired_tripwires()).
The old file is renamed, never read or printed.
"""
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def tripwire_path():
    return Path(settings.DATA_DIR) / "canary_tripwire"


def retired_tripwires():
    """The files of earlier tripwires, oldest first."""
    return sorted(Path(settings.DATA_DIR).glob("canary_tripwire.retired-*"))


class Command(BaseCommand):
    help = "Create the unpublished tripwire GUID in the private data folder (never printed)."

    def add_arguments(self, parser):
        parser.add_argument("--replace", action="store_true",
                            help="Replace an existing tripwire. Only when the old one has leaked or must be retired.")

    def handle(self, replace=False, **options):
        path = tripwire_path()
        if path.exists() and not replace:
            raise CommandError(f"A tripwire already exists at {path}. Use --replace only to retire it.")
        if path.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            retired = path.with_name(f"{path.name}.retired-{stamp}")
            os.replace(path, retired)
            os.chmod(retired, 0o600)
            self.stdout.write(f"The previous tripwire was kept as {retired} (not printed).")
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(str(uuid.uuid4()))
        os.chmod(path, 0o600)
        self.stdout.write(f"Tripwire written to {path} (not printed; keep it out of every AI service).")
