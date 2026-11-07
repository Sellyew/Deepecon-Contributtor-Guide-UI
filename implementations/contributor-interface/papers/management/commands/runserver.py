"""runserver that refuses non-loopback addresses at Stage 0 (plan §3, "Stage 0 binding")."""
from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as StaticRunserver
from django.core.management.base import CommandError

LOOPBACK = {"127.0.0.1", "localhost", "::1", "[::1]"}


class Command(StaticRunserver):
    def handle(self, *args, **options):
        if settings.STAGE == "0":
            addrport = options.get("addrport") or ""
            host = addrport.rsplit(":", 1)[0] if ":" in addrport and not addrport.isdigit() else ""
            if addrport.startswith("[") and "]" in addrport:
                host = addrport[: addrport.index("]") + 1]
            if host and host not in LOOPBACK:
                raise CommandError(f"Stage 0 serves only the loopback address; refusing to listen on {host}.")
        return super().handle(*args, **options)
