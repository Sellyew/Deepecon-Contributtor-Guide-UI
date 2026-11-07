"""Invitation, consent, authorization, and language tests (plan §2.2, §2.3, §3, §5)."""
import hashlib
import io
import re
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.staticfiles import finders
from django.contrib.sessions.models import Session
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from contributors.access import SESSION_KEY
from contributors.models import Assignment, Consent, Contributor, Invitation
from deepecon_site.testing import PrivateStorageMixin, example_json, import_example
from papers.importers import package_path
from papers.models import EventLog


class ContributorSiteTestCase(PrivateStorageMixin, TestCase):
    """Two contributors on two papers, as the plan's authorization tests require."""

    def setUp(self):
        super().setUp()
        self.empirical = import_example("empirical")
        self.theory = import_example("theory")
        self.alice = Contributor.objects.create(display_name="Alice (fictional)", preferred_language="en")
        self.bo = Contributor.objects.create(display_name="Bo (fictional)", preferred_language="zh-hans")
        self.a_emp = Assignment.objects.create(contributor=self.alice, paper=self.empirical, relationship_to_paper="author")
        self.b_th = Assignment.objects.create(contributor=self.bo, paper=self.theory, relationship_to_paper="author")
        _, self.alice_token = Invitation.issue(self.a_emp)
        _, self.bo_token = Invitation.issue(self.b_th)

    def open_link(self, token, client=None):
        return (client or self.client).get(f"/i/{token}/")

    def consent(self, paper, team_ai_use="no"):
        return self.client.post(reverse("contributors:notice", args=[paper.paper_id]),
                                {"acknowledge_evaluation": "on", "team_ai_use": team_ai_use})


class InvitationTests(ContributorSiteTestCase):
    def test_tokens_are_stored_only_as_hashes(self):
        invitation, raw = Invitation.issue(self.a_emp)
        self.assertEqual(invitation.token_hash, hashlib.sha256(raw.encode()).hexdigest())
        for row in Invitation.objects.values():
            self.assertNotIn(raw, " ".join(str(v) for v in row.values()))
        self.open_link(raw)
        self.assertNotIn(raw, str(list(EventLog.objects.values())))

    def test_link_signs_in_and_redirects_without_the_token(self):
        response = self.open_link(self.alice_token)
        self.assertRedirects(response, reverse("contributors:notice", args=[self.empirical.paper_id]))
        self.assertNotIn(self.alice_token, response["Location"])
        self.assertEqual(self.client.session[SESSION_KEY], Invitation.find_active(self.alice_token).pk)
        self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_each_use_starts_a_new_session(self):
        self.client.get("/")
        self.client.session.save()
        before = self.client.session.session_key
        self.open_link(self.alice_token)
        self.assertNotEqual(self.client.session.session_key, before)

    def test_invalid_expired_and_revoked_links_do_not_sign_in(self):
        expired, expired_raw = Invitation.issue(self.a_emp)
        expired.expires_at = timezone.now() - timedelta(minutes=1)
        expired.save()
        revoked, revoked_raw = Invitation.issue(self.a_emp)
        revoked.revoked_at = timezone.now()
        revoked.save()
        for token in ("not-a-real-token-1234567890", expired_raw, revoked_raw, "x" * 500):
            response = self.open_link(token)
            self.assertEqual(response.status_code, 404)
            self.assertContains(response, "This link does not work", status_code=404)
            self.assertNotIn(SESSION_KEY, self.client.session)

    def test_preferred_language_is_set_at_the_first_visit(self):
        self.open_link(self.bo_token)
        self.assertEqual(self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value, "zh-hans")

    def test_the_contributors_own_language_choice_survives_reopening_the_link(self):
        self.open_link(self.bo_token)
        self.client.post(reverse("set_language"), {"language": "en", "next": "/"})
        self.open_link(self.bo_token)
        self.assertEqual(self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value, "en")

    def _signed_in_with_consent(self):
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.assertEqual(self.client.get(reverse("contributors:my_paper", args=[self.empirical.paper_id])).status_code, 200)

    def _assert_session_ended(self):
        urls = ["/", *(reverse(f"contributors:{name}", args=[self.empirical.paper_id]) for name in ("notice", "my_paper", "package"))]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 403, url)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_revoking_a_link_ends_sessions_already_opened_with_it(self):
        self._signed_in_with_consent()
        Invitation.objects.filter(assignment=self.a_emp).update(revoked_at=timezone.now())
        self._assert_session_ended()

    def test_an_expired_link_ends_sessions_already_opened_with_it(self):
        self._signed_in_with_consent()
        Invitation.objects.filter(assignment=self.a_emp).update(expires_at=timezone.now() - timedelta(seconds=1))
        self._assert_session_ended()

    def test_a_link_reaches_only_its_own_assignment(self):
        a_th = Assignment.objects.create(contributor=self.alice, paper=self.theory, relationship_to_paper="invited_expert")
        self.open_link(self.alice_token)
        self.assertEqual(self.client.get(reverse("contributors:notice", args=[self.theory.paper_id])).status_code, 404)
        _, theory_token = Invitation.issue(a_th)
        self.open_link(theory_token)
        self.assertEqual(self.client.get(reverse("contributors:notice", args=[self.theory.paper_id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("contributors:notice", args=[self.empirical.paper_id])).status_code, 404)

    def test_create_invitation_command_prints_the_link_once(self):
        out = io.StringIO()
        call_command("create_invitation", self.a_emp.public_id, "--days", "3", stdout=out)
        token = re.search(r"/i/([^/\s]+)/", out.getvalue()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        with self.assertRaises(CommandError):
            call_command("create_invitation", "a-unknown", stdout=io.StringIO())

    def test_admin_action_shows_links_without_storing_them(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        response = self.client.post(reverse("admin:contributors_assignment_changelist"),
                                    {"action": "create_invitation", "_selected_action": [self.a_emp.pk]})
        self.assertEqual(response.status_code, 200)
        token = re.search(r"/i/([A-Za-z0-9_-]+)/", response.content.decode()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        self.assertIn("no-store", response["Cache-Control"])
        for session in Session.objects.all():
            self.assertNotIn(token, str(session.get_decoded()))

    def test_view_only_staff_can_neither_invite_nor_revoke(self):
        viewer = get_user_model().objects.create_user("viewer", "viewer@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.set(Permission.objects.filter(codename__in=["view_assignment", "view_invitation"]))
        self.client.force_login(viewer)
        before = Invitation.objects.count()
        self.client.post(reverse("admin:contributors_assignment_changelist"),
                         {"action": "create_invitation", "_selected_action": [self.a_emp.pk]})
        self.assertEqual(Invitation.objects.count(), before)
        self.client.post(reverse("admin:contributors_invitation_changelist"),
                         {"action": "revoke", "_selected_action": list(Invitation.objects.values_list("pk", flat=True))})
        self.assertFalse(Invitation.objects.filter(revoked_at__isnull=False).exists())

    @override_settings(STAGE="1")
    def test_demo_loader_is_refused_outside_stage_0(self):
        with self.assertRaises(CommandError):
            call_command("load_demo", stdout=io.StringIO())


class CsrfTests(ContributorSiteTestCase):
    """The test client skips CSRF checks by default; a browser does not."""

    def test_consent_form_works_with_csrf_enforced(self):
        from django.test import Client
        browser = Client(enforce_csrf_checks=True)
        self.open_link(self.alice_token, client=browser)
        url = reverse("contributors:notice", args=[self.empirical.paper_id])
        page = browser.get(url)
        self.assertEqual(page["Referrer-Policy"], "same-origin")   # "no-referrer" makes browsers send Origin: null
        token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page.content.decode()).group(1)
        response = browser.post(url, {"acknowledge_evaluation": "on", "team_ai_use": "no", "csrfmiddlewaretoken": token},
                                HTTP_ORIGIN="http://testserver")
        self.assertEqual(response.status_code, 302)
        refused = browser.post(url, {"acknowledge_evaluation": "on", "team_ai_use": "no", "csrfmiddlewaretoken": token},
                               HTTP_ORIGIN="null")
        self.assertEqual(refused.status_code, 403)


class NoticeAndConsentTests(ContributorSiteTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)

    def test_my_paper_requires_the_notice_first(self):
        response = self.client.get(reverse("contributors:my_paper", args=[self.empirical.paper_id]))
        self.assertRedirects(response, reverse("contributors:notice", args=[self.empirical.paper_id]))

    def test_notice_says_what_evaluation_does(self):
        response = self.client.get(reverse("contributors:notice", args=[self.empirical.paper_id]))
        self.assertContains(response, "sent through their APIs to each AI company whose models are evaluated")
        self.assertContains(response, "This site sends nothing to AI services")

    def test_acknowledgement_is_required(self):
        response = self.client.post(reverse("contributors:notice", args=[self.empirical.paper_id]), {"team_ai_use": "no"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Taking part requires this acknowledgement.")
        self.assertFalse(Consent.objects.exists())

    def test_consent_is_recorded_with_its_date_and_choice(self):
        response = self.consent(self.empirical, team_ai_use="yes")
        self.assertRedirects(response, reverse("contributors:my_paper", args=[self.empirical.paper_id]))
        consent = self.a_emp.latest_consent()
        self.assertTrue(consent.evaluation_through_apis_acknowledged)
        self.assertTrue(consent.team_ai_use_of_unpublished_material)
        self.assertEqual(consent.notice_version, settings.NOTICE_VERSION)
        self.assertIsNotNone(consent.recorded_at)
        self.consent(self.empirical, team_ai_use="no")                 # a change is a new record
        self.assertEqual(self.a_emp.consents.count(), 2)
        self.assertFalse(self.a_emp.latest_consent().team_ai_use_of_unpublished_material)


class AuthorizationTests(ContributorSiteTestCase):
    def test_signed_out_visitors_see_only_the_link_page(self):
        for url in ("/", reverse("contributors:my_paper", args=[self.empirical.paper_id]),
                    reverse("contributors:notice", args=[self.empirical.paper_id]),
                    reverse("contributors:package", args=[self.empirical.paper_id])):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403, url)
            self.assertContains(response, "Please use your personal link", status_code=403)

    def test_other_papers_are_refused(self):
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        for name in ("notice", "my_paper", "package"):
            response = self.client.get(reverse(f"contributors:{name}", args=[self.theory.paper_id]))
            self.assertEqual(response.status_code, 404, name)
            response = self.client.get(reverse(f"contributors:{name}", args=["no-such-paper"]))
            self.assertEqual(response.status_code, 404, name)

    def test_package_download_needs_consent_and_visibility(self):
        self.open_link(self.alice_token)
        url = reverse("contributors:package", args=[self.empirical.paper_id])
        self.assertEqual(self.client.get(url).status_code, 404)                 # no consent yet
        self.consent(self.empirical)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        body = b"".join(response.streaming_content)
        response.close()
        self.assertEqual(hashlib.sha256(body).hexdigest(), self.empirical.current_package().sha256)
        self.empirical.config = dict(self.empirical.config, candidate_package_visible_to_contributors=False)
        self.empirical.save()
        self.assertEqual(self.client.get(url).status_code, 404)
        page = self.client.get(reverse("contributors:my_paper", args=[self.empirical.paper_id]))
        self.assertNotContains(page, url)

    def test_package_shown_when_the_configuration_omits_visibility(self):
        self.empirical.config = {k: v for k, v in self.empirical.config.items()
                                 if k != "candidate_package_visible_to_contributors"}
        self.empirical.save()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        url = reverse("contributors:package", args=[self.empirical.paper_id])
        self.assertContains(self.client.get(reverse("contributors:my_paper", args=[self.empirical.paper_id])), url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_package_file_is_not_reachable_as_a_static_file(self):
        package = self.empirical.current_package()
        stored = package_path(package).resolve()
        self.assertTrue(stored.is_file())
        self.assertIsNone(finders.find(package.storage_name))
        self.assertTrue(stored.is_relative_to(Path(settings.PRIVATE_STORAGE_ROOT).resolve()))
        for static_dir in [settings.STATIC_ROOT, *settings.STATICFILES_DIRS]:
            self.assertFalse(stored.is_relative_to(Path(static_dir).resolve()), static_dir)


class MyPaperTests(ContributorSiteTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)
        self.consent(self.empirical)

    def test_shows_categories_and_no_scoring_material(self):
        response = self.client.get(reverse("contributors:my_paper", args=[self.empirical.paper_id]))
        config = example_json("empirical", "paper-config")
        for category in config["categories"]:
            self.assertContains(response, category["label"]["en"])
        rubric = example_json("empirical", "rubric")
        for forbidden in ("allowed_scores", "scoring_method", "tiers", "points", "calibration_status"):
            self.assertNotContains(response, forbidden)
        for group in ("conceptual", "missing", "technical"):
            for entry in rubric[group]:
                for value in entry.get("tiers", {}).values():
                    self.assertNotContains(response, value)

    def test_switching_language_changes_the_interface_but_not_item_text(self):
        url = reverse("contributors:my_paper", args=[self.empirical.paper_id])
        english = self.client.get(url)
        self.assertContains(english, "My paper")
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": url})
        chinese = self.client.get(url)
        self.assertContains(chinese, "我的论文")
        self.assertContains(chinese, self.empirical.title)                       # the paper's own text is not translated
        zh_label = example_json("empirical", "paper-config")["categories"][0]["label"]["zh-Hans"]
        self.assertContains(chinese, zh_label)                                    # per-paper labels come from the configuration
        self.assertNotContains(chinese, "My paper")
