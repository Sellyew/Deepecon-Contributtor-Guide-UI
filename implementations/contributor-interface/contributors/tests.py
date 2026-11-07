"""Invitation, paper choice, consent, authorization, and language tests (plan §2.2, §2.3, §3, §5; D-044)."""
import hashlib
import io
import re
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.contrib.staticfiles import finders
from django.core.management import CommandError, call_command
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from contributors.access import SESSION_KEY
from contributors.models import Assignment, Consent, Contributor, Invitation, issue_invitation
from deepecon_site.testing import PrivateStorageMixin, example_json, import_example
from papers.importers import package_path
from papers.models import EventLog


def url(name, paper):
    return reverse(f"contributors:{name}", args=[paper.paper_id])


class ContributorSiteTestCase(PrivateStorageMixin, TestCase):
    """Two authors on two papers, as the plan's authorization tests require; nothing is open to all."""

    def setUp(self):
        super().setUp()
        self.empirical = import_example("empirical")
        self.theory = import_example("theory")
        self.alice = Contributor.objects.create(display_name="Alice (fictional)", preferred_language="en")
        self.bo = Contributor.objects.create(display_name="Bo (fictional)", preferred_language="zh-hans")
        self.a_emp = self.assign(self.alice, self.empirical)
        self.b_th = self.assign(self.bo, self.theory)
        _, self.alice_token = Invitation.issue(self.alice)
        _, self.bo_token = Invitation.issue(self.bo)

    def assign(self, contributor, paper, relationship="author", current=True):
        assignment = Assignment.objects.create(contributor=contributor, paper=paper, relationship_to_paper=relationship)
        if current:
            contributor.current_assignment = assignment
            contributor.save()
        return assignment

    def open_link(self, token, client=None):
        return (client or self.client).get(f"/i/{token}/")

    def consent(self, paper, team_ai_use="no"):
        return self.client.post(url("notice", paper), {"acknowledge_evaluation": "on", "team_ai_use": team_ai_use})

    def signed_in_with_consent(self):
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 200)

    def assert_signed_out(self):
        for page in ["/", reverse("contributors:papers"), url("choose", self.empirical),
                     *(url(name, self.empirical) for name in ("notice", "my_paper", "package"))]:
            self.assertEqual(self.client.get(page).status_code, 403, page)
        self.assertNotIn(SESSION_KEY, self.client.session)


class InvitationTests(ContributorSiteTestCase):
    def test_tokens_are_stored_only_as_hashes(self):
        invitation, raw = issue_invitation(self.alice, "test")
        self.assertEqual(invitation.token_hash, hashlib.sha256(raw.encode()).hexdigest())
        for row in Invitation.objects.values():
            self.assertNotIn(raw, " ".join(str(v) for v in row.values()))
        self.open_link(raw)
        self.assertNotIn(raw, str(list(EventLog.objects.values())))

    def test_link_signs_in_and_redirects_without_the_token(self):
        response = self.open_link(self.alice_token)
        self.assertRedirects(response, url("notice", self.empirical))
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
        expired, expired_raw = Invitation.issue(self.alice)
        expired.expires_at = timezone.now() - timedelta(minutes=1)
        expired.save()
        revoked, revoked_raw = Invitation.issue(self.alice)
        revoked.revoked_at = timezone.now()
        revoked.save()
        for token in ("not-a-real-token-1234567890", expired_raw, revoked_raw, "x" * 500):
            response = self.open_link(token)
            self.assertEqual(response.status_code, 404)
            self.assertContains(response, "This link does not work", status_code=404)
            self.assertNotIn(SESSION_KEY, self.client.session)

    def test_revoking_a_link_ends_sessions_already_opened_with_it(self):
        self.signed_in_with_consent()
        Invitation.objects.filter(contributor=self.alice).update(revoked_at=timezone.now())
        self.assert_signed_out()

    def test_sessions_outlast_link_expiry(self):
        # D-044: expiry stops new sign-ins only; revocation is what ends a session.
        self.signed_in_with_consent()
        Invitation.objects.filter(contributor=self.alice).update(expires_at=timezone.now() - timedelta(seconds=1))
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 200)
        self.assertEqual(Client().get(f"/i/{self.alice_token}/").status_code, 404)    # but the link no longer opens

    def test_a_new_link_revokes_the_earlier_ones(self):
        self.signed_in_with_consent()
        _, new_raw = issue_invitation(self.alice, "test")
        self.assert_signed_out()                                  # one link at a time: the old session ends
        self.assertEqual(self.open_link(self.alice_token).status_code, 404)
        self.assertEqual(self.open_link(new_raw).status_code, 302)
        self.assertEqual(Invitation.objects.filter(contributor=self.alice, revoked_at__isnull=True).count(), 1)
        self.assertTrue(Invitation.find_active(self.bo_token))   # other contributors' links are untouched

    def test_preferred_language_is_set_at_the_first_visit(self):
        self.open_link(self.bo_token)
        self.assertEqual(self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value, "zh-hans")

    def test_the_contributors_own_language_choice_survives_reopening_the_link(self):
        self.open_link(self.bo_token)
        self.client.post(reverse("set_language"), {"language": "en", "next": "/"})
        self.open_link(self.bo_token)
        self.assertEqual(self.client.cookies[settings.LANGUAGE_COOKIE_NAME].value, "en")

    def test_create_invitation_command_prints_the_link_once(self):
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        out = io.StringIO()
        call_command("create_invitation", a_th.public_id, "--days", "3", stdout=out)
        token = re.search(r"/i/([^/\s]+)/", out.getvalue()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, a_th)       # an assignment's link opens that paper
        self.assertIsNone(Invitation.find_active(self.alice_token))  # and the earlier link is revoked
        out = io.StringIO()
        call_command("create_invitation", self.bo.public_id, stdout=out)
        self.assertIn(self.theory.paper_id, out.getvalue())
        with self.assertRaises(CommandError):
            call_command("create_invitation", "a-unknown", stdout=io.StringIO())

    def test_admin_actions_show_links_without_storing_them(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        response = self.client.post(reverse("admin:contributors_assignment_changelist"),
                                    {"action": "create_invitation", "_selected_action": [a_th.pk]})
        self.assertEqual(response.status_code, 200)
        token = re.search(r"/i/([A-Za-z0-9_-]+)/", response.content.decode()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        self.assertIn("no-store", response["Cache-Control"])
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, a_th)
        for session in Session.objects.all():
            self.assertNotIn(token, str(session.get_decoded()))
        response = self.client.post(reverse("admin:contributors_contributor_changelist"),
                                    {"action": "create_invitation", "_selected_action": [self.alice.pk]})
        self.assertEqual(response.status_code, 200)
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, a_th)       # a contributor's link keeps their paper

    def test_one_admin_link_per_contributor(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        before = Invitation.objects.count()
        self.client.post(reverse("admin:contributors_assignment_changelist"),
                         {"action": "create_invitation", "_selected_action": [self.a_emp.pk, a_th.pk]})
        self.assertEqual(Invitation.objects.count(), before)

    def test_view_only_staff_can_neither_invite_nor_revoke(self):
        viewer = get_user_model().objects.create_user("viewer", "viewer@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.set(Permission.objects.filter(
            codename__in=["view_assignment", "view_contributor", "view_invitation"]))
        self.client.force_login(viewer)
        before = Invitation.objects.count()
        self.client.post(reverse("admin:contributors_assignment_changelist"),
                         {"action": "create_invitation", "_selected_action": [self.a_emp.pk]})
        self.client.post(reverse("admin:contributors_contributor_changelist"),
                         {"action": "create_invitation", "_selected_action": [self.alice.pk]})
        self.assertEqual(Invitation.objects.count(), before)
        self.client.post(reverse("admin:contributors_invitation_changelist"),
                         {"action": "revoke", "_selected_action": list(Invitation.objects.values_list("pk", flat=True))})
        self.assertFalse(Invitation.objects.filter(revoked_at__isnull=False).exists())

    @override_settings(STAGE="1")
    def test_demo_loader_is_refused_outside_stage_0(self):
        with self.assertRaises(CommandError):
            call_command("load_demo", stdout=io.StringIO())


class PaperChoiceTests(ContributorSiteTestCase):
    """D-044: the link opens one paper at a time, chosen by the contributor from the papers offered."""

    def setUp(self):
        super().setUp()
        self.carol = Contributor.objects.create(display_name="Carol (fictional)")
        _, self.carol_token = Invitation.issue(self.carol)

    def open_pool(self, *papers):
        for paper in papers:
            paper.in_pool = True
            paper.save()

    def choose(self, paper, client=None):
        return (client or self.client).post(url("choose", paper))

    def test_without_a_paper_the_link_leads_to_the_choice(self):
        self.open_pool(self.empirical, self.theory)
        self.assertRedirects(self.open_link(self.carol_token), reverse("contributors:papers"))
        self.assertRedirects(self.client.get("/"), reverse("contributors:papers"))
        page = self.client.get(reverse("contributors:papers"))
        self.assertContains(page, self.empirical.title)
        self.assertContains(page, self.theory.title)

    def test_the_list_shows_citations_only(self):
        self.open_pool(self.empirical)
        self.open_link(self.carol_token)
        page = self.client.get(reverse("contributors:papers")).content.decode()
        rubric = example_json("empirical", "rubric")
        for entry in rubric["conceptual"] + rubric["missing"] + rubric["technical"]:
            for value in entry.values():
                if isinstance(value, str) and len(value) > 20:
                    self.assertNotIn(value, page)
        self.assertNotIn(url("package", self.empirical), page)

    def test_only_offered_papers_can_be_chosen(self):
        self.open_link(self.carol_token)                         # nothing is open to all, nothing assigned
        self.assertNotContains(self.client.get(reverse("contributors:papers")), self.empirical.title)
        for name in ("choose", "notice", "my_paper", "package"):
            self.assertEqual(self.client.get(url(name, self.empirical)).status_code, 404, name)
        self.assertEqual(self.choose(self.empirical).status_code, 404)
        self.assertFalse(Assignment.objects.filter(contributor=self.carol).exists())

    def test_choosing_fixes_the_link_on_that_paper(self):
        self.open_pool(self.empirical, self.theory)
        self.open_link(self.carol_token)
        self.assertContains(self.client.get(url("choose", self.theory)), "Work on this paper")
        self.assertFalse(Assignment.objects.filter(contributor=self.carol).exists())     # a GET changes nothing
        self.assertRedirects(self.choose(self.theory), url("my_paper", self.theory), target_status_code=302)
        assignment = Assignment.objects.get(contributor=self.carol)
        self.assertEqual((assignment.paper, assignment.relationship_to_paper, assignment.added_by),
                         (self.theory, "invited_expert", Assignment.BY_CONTRIBUTOR))
        event = EventLog.objects.get(operation="paper_chosen")
        self.assertEqual(event.details["previous_assignment"], None)
        fresh = Client()
        self.assertRedirects(self.open_link(self.carol_token, client=fresh), url("notice", self.theory))
        self.assertEqual(fresh.get(url("notice", self.empirical)).status_code, 302)        # not the current paper

    def test_changing_paper_keeps_the_earlier_work(self):
        self.open_pool(self.theory)
        self.signed_in_with_consent()                             # Alice, author of the empirical paper
        self.choose(self.theory)
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment.paper, self.theory)
        self.assertRedirects(self.client.get(url("my_paper", self.empirical)), url("choose", self.empirical))
        page = self.client.get(reverse("contributors:papers"))
        self.assertContains(page, "You have worked on this paper before")
        self.choose(self.empirical)                               # back to her own paper: consent is kept
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 200)
        self.assertEqual(self.a_emp.consents.count(), 1)
        self.assertEqual(Assignment.objects.filter(contributor=self.alice, paper=self.empirical).get().relationship_to_paper,
                         "author")
        self.assertEqual(EventLog.objects.filter(operation="paper_chosen").count(), 2)

    def test_a_paper_closed_to_all_stays_open_to_those_who_chose_it(self):
        self.open_pool(self.theory)
        self.open_link(self.carol_token)
        self.choose(self.theory)
        self.theory.in_pool = False
        self.theory.save()
        self.assertContains(self.client.get(url("notice", self.theory)), self.theory.title)
        dave = Contributor.objects.create(display_name="Dave (fictional)")
        _, dave_token = Invitation.issue(dave)
        other = Client()
        self.open_link(dave_token, client=other)
        self.assertEqual(other.get(url("choose", self.theory)).status_code, 404)

    def test_several_contributors_may_choose_the_same_paper(self):
        self.open_pool(self.empirical)
        self.open_link(self.carol_token)
        self.choose(self.empirical)
        self.open_link(self.bo_token)
        self.choose(self.empirical)
        self.assertEqual(Assignment.objects.filter(paper=self.empirical).count(), 3)

    def test_choosing_needs_a_csrf_token(self):
        self.open_pool(self.theory)
        browser = Client(enforce_csrf_checks=True)
        self.open_link(self.carol_token, client=browser)
        self.assertEqual(self.choose(self.theory, client=browser).status_code, 403)
        page = browser.get(url("choose", self.theory))
        token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page.content.decode()).group(1)
        response = browser.post(url("choose", self.theory), {"csrfmiddlewaretoken": token}, HTTP_ORIGIN="http://testserver")
        self.assertEqual(response.status_code, 302)

    def test_my_paper_offers_another_choice(self):
        self.signed_in_with_consent()
        self.assertContains(self.client.get(url("my_paper", self.empirical)), reverse("contributors:papers"))

    def test_a_current_paper_of_another_contributor_is_ignored(self):
        self.carol.current_assignment = self.a_emp                # inconsistent data must not grant access
        self.carol.save()
        self.open_link(self.carol_token)
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 404)


class CsrfTests(ContributorSiteTestCase):
    """The test client skips CSRF checks by default; a browser does not."""

    def test_consent_form_works_with_csrf_enforced(self):
        browser = Client(enforce_csrf_checks=True)
        self.open_link(self.alice_token, client=browser)
        page = browser.get(url("notice", self.empirical))
        self.assertEqual(page["Referrer-Policy"], "same-origin")   # "no-referrer" makes browsers send Origin: null
        token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page.content.decode()).group(1)
        response = browser.post(url("notice", self.empirical),
                                {"acknowledge_evaluation": "on", "team_ai_use": "no", "csrfmiddlewaretoken": token},
                                HTTP_ORIGIN="http://testserver")
        self.assertEqual(response.status_code, 302)
        refused = browser.post(url("notice", self.empirical),
                               {"acknowledge_evaluation": "on", "team_ai_use": "no", "csrfmiddlewaretoken": token},
                               HTTP_ORIGIN="null")
        self.assertEqual(refused.status_code, 403)


class NoticeAndConsentTests(ContributorSiteTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)

    def test_my_paper_requires_the_notice_first(self):
        self.assertRedirects(self.client.get(url("my_paper", self.empirical)), url("notice", self.empirical))

    def test_notice_says_what_evaluation_does(self):
        response = self.client.get(url("notice", self.empirical))
        self.assertContains(response, "sent through their APIs to each AI company whose models are evaluated")
        self.assertContains(response, "This site sends nothing to AI services")
        self.assertContains(response, "built from your paper")

    def test_invited_experts_see_wording_for_someone_elses_paper(self):
        self.a_emp.relationship_to_paper = "invited_expert"
        self.a_emp.save()
        response = self.client.get(url("notice", self.empirical))
        self.assertContains(response, "built from this paper")
        self.assertContains(response, "built from this paper&#x27;s package and the reviews")
        self.assertNotContains(response, "your paper")
        self.assertNotContains(response, "my package")
        self.consent(self.empirical)
        self.assertEqual(self.a_emp.latest_consent().notice_version, f"{settings.NOTICE_VERSION}/expert")

    def test_acknowledgement_is_required(self):
        response = self.client.post(url("notice", self.empirical), {"team_ai_use": "no"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Taking part requires this acknowledgement.")
        self.assertFalse(Consent.objects.exists())

    def test_consent_is_recorded_with_its_date_and_choice(self):
        response = self.consent(self.empirical, team_ai_use="yes")
        self.assertRedirects(response, url("my_paper", self.empirical))
        consent = self.a_emp.latest_consent()
        self.assertTrue(consent.evaluation_through_apis_acknowledged)
        self.assertTrue(consent.team_ai_use_of_unpublished_material)
        self.assertEqual(consent.notice_version, f"{settings.NOTICE_VERSION}/author")
        self.assertIsNotNone(consent.recorded_at)
        self.consent(self.empirical, team_ai_use="no")                 # a change is a new record
        self.assertEqual(self.a_emp.consents.count(), 2)
        self.assertFalse(self.a_emp.latest_consent().team_ai_use_of_unpublished_material)


class AuthorizationTests(ContributorSiteTestCase):
    def test_signed_out_visitors_see_only_the_link_page(self):
        for page in ("/", reverse("contributors:papers"), url("choose", self.empirical),
                     url("my_paper", self.empirical), url("notice", self.empirical), url("package", self.empirical)):
            response = self.client.get(page)
            self.assertEqual(response.status_code, 403, page)
            self.assertContains(response, "Please use your personal link", status_code=403)

    def test_other_papers_are_refused(self):
        self.signed_in_with_consent()
        for name in ("choose", "notice", "my_paper", "package"):
            self.assertEqual(self.client.get(url(name, self.theory)).status_code, 404, name)
            self.assertEqual(self.client.get(reverse(f"contributors:{name}", args=["no-such-paper"])).status_code, 404, name)

    def test_package_download_needs_consent_and_visibility(self):
        self.open_link(self.alice_token)
        package = url("package", self.empirical)
        self.assertEqual(self.client.get(package).status_code, 404)                 # no consent yet
        self.consent(self.empirical)
        response = self.client.get(package)
        self.assertEqual(response.status_code, 200)
        body = b"".join(response.streaming_content)
        response.close()
        self.assertEqual(hashlib.sha256(body).hexdigest(), self.empirical.current_package().sha256)
        self.empirical.config = dict(self.empirical.config, candidate_package_visible_to_contributors=False)
        self.empirical.save()
        self.assertEqual(self.client.get(package).status_code, 404)
        self.assertNotContains(self.client.get(url("my_paper", self.empirical)), package)

    def test_package_shown_when_the_configuration_omits_visibility(self):
        self.empirical.config = {k: v for k, v in self.empirical.config.items()
                                 if k != "candidate_package_visible_to_contributors"}
        self.empirical.save()
        self.signed_in_with_consent()
        self.assertContains(self.client.get(url("my_paper", self.empirical)), url("package", self.empirical))
        response = self.client.get(url("package", self.empirical))
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
        self.signed_in_with_consent()

    def test_shows_categories_and_no_scoring_material(self):
        response = self.client.get(url("my_paper", self.empirical))
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
        page = url("my_paper", self.empirical)
        self.assertContains(self.client.get(page), "My paper")
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": page})
        chinese = self.client.get(page)
        self.assertContains(chinese, "我的论文")
        self.assertContains(chinese, self.empirical.title)                       # the paper's own text is not translated
        zh_label = example_json("empirical", "paper-config")["categories"][0]["label"]["zh-Hans"]
        self.assertContains(chinese, zh_label)                                    # per-paper labels come from the configuration
        self.assertNotContains(chinese, "My paper")


class LinkMigrationTests(TransactionTestCase):
    """contributors 0002 moves links from assignments to contributors and keeps the paper they opened."""

    def test_existing_links_keep_opening_their_paper(self):
        from django.db import connection
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)
        old = [("contributors", "0001_initial"), ("papers", "0001_initial")]
        executor.migrate(old)
        apps = executor.loader.project_state(old).apps
        Paper = apps.get_model("papers", "Paper")
        Contributor_ = apps.get_model("contributors", "Contributor")
        Assignment_ = apps.get_model("contributors", "Assignment")
        Invitation_ = apps.get_model("contributors", "Invitation")
        first = Paper.objects.create(paper_id="p-one", title="One", config={}, config_sha256="0" * 64)
        second = Paper.objects.create(paper_id="p-two", title="Two", config={}, config_sha256="1" * 64)
        person = Contributor_.objects.create(public_id="c-test", display_name="Test (fictional)")
        a1 = Assignment_.objects.create(public_id="a-one", contributor=person, paper=first, relationship_to_paper="author")
        a2 = Assignment_.objects.create(public_id="a-two", contributor=person, paper=second, relationship_to_paper="author")
        Invitation_.objects.create(assignment=a1, token_hash="a" * 64, expires_at=timezone.now())
        Invitation_.objects.create(assignment=a2, token_hash="b" * 64, expires_at=timezone.now())

        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        latest = executor.loader.graph.leaf_nodes()
        executor.migrate(latest)
        apps = executor.loader.project_state(latest).apps
        person = apps.get_model("contributors", "Contributor").objects.get(public_id="c-test")
        self.assertEqual(apps.get_model("contributors", "Invitation").objects.filter(contributor=person).count(), 2)
        self.assertEqual(person.current_assignment.public_id, "a-two")           # the most recent link's paper
