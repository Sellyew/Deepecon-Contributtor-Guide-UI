"""Site-wide privacy and security controls (plan §3)."""
import ast
import io
import logging
import re
from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from contributors.models import Assignment, Contributor, Invitation
from deepecon_site import gateway
from deepecon_site.logging_filters import RedactInvitationTokens
from deepecon_site.testing import PrivateStorageMixin, import_example

EXTERNAL = re.compile(r"""(?:src|href|action)\s*=\s*["']\s*(?:https?:)?//""", re.I)
NETWORK_MODULES = {"socket", "ssl", "http.client", "urllib.request", "urllib3", "requests", "httpx", "aiohttp",
                   "smtplib", "ftplib", "django.core.mail", "openai", "anthropic"}


def imported_names(source):
    """Every module name a source file imports, including `from x import y` as x.y."""
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            yield from (a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            yield node.module
            yield from (f"{node.module}.{a.name}" for a in node.names)


def opens_network(source):
    return any(n == m or n.startswith(m + ".") for n in imported_names(source) for m in NETWORK_MODULES)


def project_modules():
    """The site's own code, and the rubric checks it runs; not the virtual environment."""
    root = Path(settings.BASE_DIR)
    paths = [root / "manage.py", Path(settings.VALIDATION_DIR) / "rubric_checks.py"]
    for app in ("deepecon_site", "papers", "contributors"):
        paths += [p for p in (root / app).rglob("*.py")
                  if "migrations" not in p.parts and p.name not in ("tests.py", "testing.py")]
    return paths


class HeaderAndAssetTests(PrivateStorageMixin, TestCase):
    def setUp(self):
        super().setUp()
        paper = import_example("empirical")
        contributor = Contributor.objects.create(display_name="Test (fictional)")
        self.assignment = Assignment.objects.create(contributor=contributor, paper=paper, relationship_to_paper="author")
        _, token = Invitation.issue(self.assignment)
        self.client.get(f"/i/{token}/")
        self.client.post(reverse("contributors:notice", args=[paper.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        self.pages = ["/", reverse("contributors:notice", args=[paper.paper_id]),
                      reverse("contributors:my_paper", args=[paper.paper_id]), "/i/not-a-valid-token-000000/"]

    def test_security_headers(self):
        for url in self.pages:
            response = self.client.get(url, follow=True)
            csp = response["Content-Security-Policy"]
            self.assertIn("default-src 'self'", csp, url)
            self.assertNotIn("unsafe-inline", csp, url)
            self.assertEqual(response["X-Frame-Options"], "DENY")
            self.assertEqual(response["X-Content-Type-Options"], "nosniff")
            expected = "no-referrer" if url.startswith("/i/") else "same-origin"
            self.assertEqual(response["Referrer-Policy"], expected, url)
            self.assertEqual(response["Cache-Control"], "no-store")

    def test_pages_load_nothing_from_other_sites(self):
        for url in self.pages:
            html = self.client.get(url, follow=True).content.decode()
            self.assertIsNone(EXTERNAL.search(html), url)
        css = (Path(settings.BASE_DIR) / "static" / "site.css").read_text(encoding="utf-8")
        self.assertNotIn("http", css)
        self.assertNotIn("@import", css)


class GatewayTests(SimpleTestCase):
    def test_gateway_refuses_every_call(self):
        with self.assertRaises(gateway.ModelGatewayDisabled):
            gateway.call_model("any prompt", model="any")

    def test_no_module_opens_network_connections(self):
        offenders = [str(p) for p in project_modules() if opens_network(p.read_text(encoding="utf-8"))]
        self.assertEqual(offenders, [])

    def test_the_scan_catches_every_import_form(self):
        for source in ("import socket", "import os, socket", "from urllib import request", "from http import client",
                       "import urllib.request as r", "from django.core.mail import send_mail", "import anthropic"):
            self.assertTrue(opens_network(source), source)
        self.assertFalse(opens_network("import json\nfrom pathlib import Path\nfrom . import socket"))


class LoggingTests(TestCase):
    def test_filter_redacts_tokens(self):
        record = logging.LogRecord("django.server", logging.INFO, __file__, 1, '"%s" %s %s',
                                   ("GET /i/SECRETTOKEN123/ HTTP/1.1", "302", "0"), None)
        RedactInvitationTokens().filter(record)
        self.assertNotIn("SECRETTOKEN123", record.getMessage())
        self.assertIn("/i/[redacted]", record.getMessage())

    def test_server_log_is_redacted(self):
        with self.assertLogs("django.server", level="INFO") as captured:
            logging.getLogger("django.server").info('"%s" %s %s', "GET /i/SECRETTOKEN123/ HTTP/1.1", "302", "0")
        self.assertNotIn("SECRETTOKEN123", "\n".join(captured.output))

    @override_settings(DEBUG=True)
    def test_csrf_log_never_contains_tokens(self):
        # django.security.csrf logs request paths; the filter on the console handler must catch them.
        token = "RAWSECRETTOKEN0123456789abcdefXYZ"
        handlers = [h for h in logging.getLogger("django").handlers if isinstance(h, logging.StreamHandler)]
        self.assertTrue(handlers)
        stream = io.StringIO()
        old = [h.setStream(stream) for h in handlers]
        try:
            Client(enforce_csrf_checks=True).post(f"/i/{token}/")
        finally:
            for handler, previous in zip(handlers, old):
                handler.setStream(previous)
        self.assertIn("/i/[redacted]", stream.getvalue())
        self.assertNotIn(token, stream.getvalue())

    def test_request_logs_never_contain_tokens(self):
        token = "AnInvalidTokenThatMustNotBeLogged123"
        with self.assertLogs("django.request", level="WARNING") as captured:
            self.client.get(f"/i/{token}/")
        self.assertTrue(captured.output)
        self.assertNotIn(token, "\n".join(captured.output))


class PrivateStorageSettingsTests(SimpleTestCase):
    """The real setting, not the temporary one the other tests use."""

    def test_private_storage_is_outside_every_static_folder(self):
        private = Path(settings.PRIVATE_STORAGE_ROOT).resolve()
        for public in (Path(settings.STATIC_ROOT), *map(Path, settings.STATICFILES_DIRS)):
            public = public.resolve()
            self.assertFalse(private.is_relative_to(public) or public.is_relative_to(private), public)


class DatabaseSettingsTests(SimpleTestCase):
    def test_sqlite_uses_wal(self):
        self.assertIn("journal_mode=WAL", settings.DATABASES["default"]["OPTIONS"]["init_command"])
