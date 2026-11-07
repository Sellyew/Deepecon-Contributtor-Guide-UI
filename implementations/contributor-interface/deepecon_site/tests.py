"""Site-wide privacy and security controls (plan §3)."""
import logging
import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from contributors.models import Assignment, Contributor, Invitation
from deepecon_site import gateway
from deepecon_site.logging_filters import RedactInvitationTokens
from deepecon_site.testing import PrivateStorageMixin, import_example

EXTERNAL = re.compile(r"""(?:src|href|action)\s*=\s*["']\s*(?:https?:)?//""", re.I)
NETWORK_IMPORTS = re.compile(
    r"^\s*(?:import|from)\s+(requests|httpx|aiohttp|urllib3|socket|smtplib|ftplib|http\.client|urllib\.request|openai|anthropic)\b",
    re.M,
)


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
        root = Path(settings.BASE_DIR)
        offenders = []
        for path in root.rglob("*.py"):
            if "migrations" in path.parts or path.name in ("tests.py", "testing.py") or "data" in path.relative_to(root).parts:
                continue
            if NETWORK_IMPORTS.search(path.read_text(encoding="utf-8")):
                offenders.append(str(path.relative_to(root)))
        self.assertEqual(offenders, [])


class LoggingTests(TestCase):
    def test_filter_redacts_tokens(self):
        record = logging.LogRecord("django.server", logging.INFO, __file__, 1, '"%s" %s %s',
                                   ("GET /i/SECRETTOKEN123/ HTTP/1.1", "302", "0"), None)
        RedactInvitationTokens().filter(record)
        self.assertNotIn("SECRETTOKEN123", record.getMessage())
        self.assertIn("/i/[redacted]", record.getMessage())

    def test_request_logs_never_contain_tokens(self):
        token = "AnInvalidTokenThatMustNotBeLogged123"
        with self.assertLogs("django.request", level="WARNING") as captured:
            self.client.get(f"/i/{token}/")
        self.assertTrue(captured.output)
        self.assertNotIn(token, "\n".join(captured.output))


class DatabaseSettingsTests(SimpleTestCase):
    def test_sqlite_uses_wal(self):
        self.assertIn("journal_mode=WAL", settings.DATABASES["default"]["OPTIONS"]["init_command"])
