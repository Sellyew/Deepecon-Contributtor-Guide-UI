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
from papers.models import EventLog, Paper


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
        carol = Contributor.objects.create(display_name="Carol (fictional)")
        a_c = self.assign(carol, self.theory, relationship="invited_expert", current=False)
        out = io.StringIO()
        call_command("create_invitation", a_c.public_id, "--days", "3", stdout=out)
        token = re.search(r"/i/([^/\s]+)/", out.getvalue()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        carol.refresh_from_db()
        self.assertEqual(carol.current_assignment, a_c)             # with no current paper, it opens this one
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        out = io.StringIO()
        call_command("create_invitation", a_th.public_id, stdout=out)
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, self.a_emp)  # the paper she has stays (D-044)
        self.assertIn("kept the contributor's current paper", out.getvalue())
        self.assertIsNone(Invitation.find_active(self.alice_token))  # and the earlier link is revoked
        out = io.StringIO()
        call_command("create_invitation", self.bo.public_id, stdout=out)
        self.assertIn(self.theory.paper_id, out.getvalue())
        with self.assertRaises(CommandError):
            call_command("create_invitation", "a-unknown", stdout=io.StringIO())

    def test_admin_actions_show_links_without_storing_them(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        carol = Contributor.objects.create(display_name="Carol (fictional)")
        a_c = self.assign(carol, self.theory, relationship="invited_expert", current=False)
        response = self.client.post(reverse("admin:contributors_assignment_changelist"),
                                    {"action": "create_invitation", "_selected_action": [a_c.pk]})
        self.assertEqual(response.status_code, 200)
        token = re.search(r"/i/([A-Za-z0-9_-]+)/", response.content.decode()).group(1)
        self.assertTrue(Invitation.objects.filter(token_hash=hashlib.sha256(token.encode()).hexdigest()).exists())
        self.assertIn("no-store", response["Cache-Control"])
        carol.refresh_from_db()
        self.assertEqual(carol.current_assignment, a_c)
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        response = self.client.post(reverse("admin:contributors_assignment_changelist"),
                                    {"action": "create_invitation", "_selected_action": [a_th.pk]})
        self.assertContains(response, "kept the contributor&#x27;s current paper")
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, self.a_emp)  # the team does not move her link
        for session in Session.objects.all():
            self.assertNotIn(token, str(session.get_decoded()))
        response = self.client.post(reverse("admin:contributors_contributor_changelist"),
                                    {"action": "create_invitation", "_selected_action": [self.alice.pk]})
        self.assertEqual(response.status_code, 200)
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.current_assignment, self.a_emp)  # a contributor's link keeps their paper

    def test_one_admin_link_per_contributor(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        a_th = self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        before = Invitation.objects.count()
        self.client.post(reverse("admin:contributors_assignment_changelist"),
                         {"action": "create_invitation", "_selected_action": [self.a_emp.pk, a_th.pk]})
        self.assertEqual(Invitation.objects.count(), before)

    def test_links_page_warns_when_there_is_nothing_to_choose(self):
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        carol = Contributor.objects.create(display_name="Carol (fictional)")
        response = self.client.post(reverse("admin:contributors_contributor_changelist"),
                                    {"action": "create_invitation", "_selected_action": [carol.pk]})
        self.assertContains(response, "nothing to choose yet")

    def test_an_assignments_contributor_and_paper_cannot_be_changed(self):
        # Consent (and, from M2, reviews) belong to the assignment and must not move.
        self.signed_in_with_consent()
        admin = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(admin)
        response = self.client.post(reverse("admin:contributors_assignment_change", args=[self.a_emp.pk]), {
            "contributor": self.bo.pk, "paper": self.theory.pk, "relationship_to_paper": "invited_expert"})
        self.assertEqual(response.status_code, 302)
        self.a_emp.refresh_from_db()
        self.assertEqual((self.a_emp.contributor, self.a_emp.paper, self.a_emp.relationship_to_paper),
                         (self.alice, self.empirical, "invited_expert"))   # authorship stays editable
        self.assertEqual(self.a_emp.consents.count(), 1)

    def test_opening_a_link_is_logged(self):
        self.open_link(self.alice_token)
        self.assertTrue(EventLog.objects.filter(operation="invitation_used", actor=self.alice.public_id).exists())

    def test_sessions_last_while_they_are_used(self):
        # P-060: a session ends on revocation, or after SESSION_COOKIE_AGE (a year) without use;
        # every request renews it.
        self.assertGreaterEqual(settings.SESSION_COOKIE_AGE, 365 * 24 * 3600)
        self.signed_in_with_consent()
        Invitation.objects.filter(contributor=self.alice).update(expires_at=timezone.now() - timedelta(days=60))
        key = self.client.session.session_key
        Session.objects.filter(session_key=key).update(expire_date=timezone.now() + timedelta(hours=1))
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 200)
        renewed = Session.objects.get(session_key=key).expire_date
        self.assertGreater(renewed, timezone.now() + timedelta(days=360))

    def test_demo_loader_can_run_twice(self):
        for _ in range(2):
            call_command("load_demo", stdout=io.StringIO())
        demo = Contributor.objects.filter(display_name__startswith=("Demo")) | Contributor.objects.filter(display_name__startswith="示例")
        self.assertEqual(demo.count(), 3)
        for contributor in demo:
            self.assertEqual(contributor.invitations.filter(revoked_at__isnull=True).count(), 1, contributor)
        self.assertEqual(set(Paper.objects.filter(in_pool=True).values_list("paper_id", flat=True)),
                         {self.empirical.paper_id, self.theory.paper_id})
        expert = Contributor.objects.get(display_name__startswith="Demo invited expert")
        self.assertIsNone(expert.current_assignment)

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
        self.assertContains(page, "You have opened this paper before")
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

    def test_my_paper_and_the_notice_offer_another_choice(self):
        link = f'href="{reverse("contributors:papers")}"'
        self.open_link(self.alice_token)
        self.assertContains(self.client.get(url("notice", self.empirical)), link)
        self.consent(self.empirical)
        self.assertContains(self.client.get(url("my_paper", self.empirical)), link)

    def test_the_current_paper_is_listed_once(self):
        self.open_pool(self.empirical, self.theory)
        self.signed_in_with_consent()
        page = self.client.get(reverse("contributors:papers")).content.decode()
        self.assertEqual(page.count(self.empirical.title), 1)
        self.assertNotIn(url("choose", self.empirical), page)

    def test_choosing_the_current_paper_changes_nothing(self):
        self.signed_in_with_consent()
        self.assertRedirects(self.choose(self.empirical), url("my_paper", self.empirical))
        self.assertFalse(EventLog.objects.filter(operation="paper_chosen").exists())

    def test_an_empty_list_says_so(self):
        self.open_link(self.carol_token)
        self.assertContains(self.client.get(reverse("contributors:papers")), "No papers are open to you yet")

    def test_a_current_paper_of_another_contributor_is_ignored(self):
        self.carol.current_assignment = self.a_emp                # inconsistent data must not grant access
        self.carol.save()
        self.open_link(self.carol_token)
        self.assertEqual(self.client.get(url("my_paper", self.empirical)).status_code, 404)


class DangerZoneTests(ContributorSiteTestCase):
    """D-045: the team moves a contributor's link only on their request, after GitHub-style confirmation."""

    def setUp(self):
        super().setUp()
        self.empirical.in_pool = True
        self.empirical.save()
        self.team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.team_client = Client()
        self.team_client.force_login(self.team)
        self.move_url = reverse("admin:contributors_contributor_move_link", args=[self.bo.pk])

    def post(self, **data):
        form = {"step": "3", "target": self.empirical.paper_id, "requested_on": "2026-11-07",
                "request_channel": "email", "confirmation": self.bo.public_id}
        form.update(data)
        return self.team_client.post(self.move_url, form)

    def test_the_contributor_page_shows_the_danger_zone(self):
        page = self.team_client.get(reverse("admin:contributors_contributor_change", args=[self.bo.pk]))
        self.assertContains(page, "Danger zone")
        self.assertContains(page, self.move_url)

    def test_the_steps_change_nothing_until_confirmed(self):
        for step in ("1", "2", "3"):
            page = self.team_client.get(self.move_url, {"step": step})
            self.assertEqual(page.status_code, 200, step)
        self.assertContains(self.team_client.get(self.move_url, {"step": "2"}), "I have read and understand these effects")
        self.assertContains(self.team_client.get(self.move_url, {"step": "3"}), f"type “<code>{self.bo.public_id}</code>”")
        self.bo.refresh_from_db()
        self.assertEqual(self.bo.current_assignment, self.b_th)

    def test_a_wrong_confirmation_moves_nothing(self):
        for typed in ("", self.bo.public_id.upper(), self.bo.public_id + " ", self.alice.public_id):
            response = self.post(confirmation=typed)
            self.assertEqual(response.status_code, 200, typed)
        self.assertContains(self.post(confirmation="nope"), f"Type {self.bo.public_id} exactly to confirm.")
        self.bo.refresh_from_db()
        self.assertEqual(self.bo.current_assignment, self.b_th)
        self.assertFalse(EventLog.objects.filter(operation__endswith="_on_request").exists())

    def test_moving_on_request_is_recorded(self):
        _, token = Invitation.issue(self.bo)
        self.open_link(token)
        self.consent(self.theory)
        self.assertRedirects(self.post(), reverse("admin:contributors_contributor_change", args=[self.bo.pk]))
        self.bo.refresh_from_db()
        self.assertEqual(self.bo.current_assignment.paper, self.empirical)
        event = EventLog.objects.get(operation="link_moved_on_request")
        self.assertEqual((event.actor, event.details["requested_on"], event.details["request_channel"],
                          event.details["previous_assignment"]), ("team", "2026-11-07", "email", self.b_th.public_id))
        # The contributor's open session follows at once; earlier work stays.
        self.assertRedirects(self.client.get("/"), url("my_paper", self.empirical), target_status_code=302)
        self.assertEqual(self.b_th.consents.count(), 1)

    def test_rewind_sends_the_link_back_to_the_list(self):
        self.post(target="rewind", request_channel="wechat")
        self.bo.refresh_from_db()
        self.assertIsNone(self.bo.current_assignment)
        self.assertTrue(EventLog.objects.filter(operation="link_rewound_on_request").exists())
        _, token = Invitation.issue(self.bo)
        self.assertRedirects(self.open_link(token), reverse("contributors:papers"))

    def test_only_papers_offered_to_the_contributor_are_targets(self):
        self.empirical.in_pool = False
        self.empirical.save()
        self.assertEqual(self.post().status_code, 200)              # not a valid choice any more
        self.bo.refresh_from_db()
        self.assertEqual(self.bo.current_assignment, self.b_th)

    def test_a_request_cannot_be_dated_in_the_future(self):
        later = (timezone.localdate() + timedelta(days=2)).isoformat()
        self.assertContains(self.post(requested_on=later), "cannot be in the future")

    def test_staff_without_change_permission_cannot_move_links(self):
        viewer = get_user_model().objects.create_user("viewer", "viewer@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.set(Permission.objects.filter(codename="view_contributor"))
        other = Client()
        other.force_login(viewer)
        with self.assertLogs("django.request", level="WARNING"):
            self.assertEqual(other.get(self.move_url).status_code, 403)
        with self.assertLogs("django.request", level="WARNING"):
            other.post(self.move_url, {"step": "3", "target": self.empirical.paper_id, "requested_on": "2026-11-07",
                                       "request_channel": "email", "confirmation": self.bo.public_id})
        self.bo.refresh_from_db()
        self.assertEqual(self.bo.current_assignment, self.b_th)
        page = other.get(reverse("admin:contributors_contributor_change", args=[self.bo.pk]))
        self.assertNotContains(page, "Danger zone")


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
    """contributors 0002 moves links from assignments to contributors (one working link each)."""

    OLD = [("contributors", "0001_initial"), ("papers", "0001_initial")]

    def executor(self):
        from django.db import connection
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        return executor

    def latest(self, executor):
        return executor.loader.graph.leaf_nodes()

    def test_each_contributor_keeps_their_newest_working_link(self):
        executor = self.executor()
        executor.migrate(self.OLD)
        apps = executor.loader.project_state(self.OLD).apps
        Paper_ = apps.get_model("papers", "Paper")
        Contributor_ = apps.get_model("contributors", "Contributor")
        Assignment_ = apps.get_model("contributors", "Assignment")
        Invitation_ = apps.get_model("contributors", "Invitation")
        later, past = timezone.now() + timedelta(days=30), timezone.now() - timedelta(days=1)
        one = Paper_.objects.create(paper_id="p-one", title="One", config={}, config_sha256="0" * 64)
        two = Paper_.objects.create(paper_id="p-two", title="Two", config={}, config_sha256="1" * 64)

        def person(pid, links):
            contributor = Contributor_.objects.create(public_id=pid, display_name="Test (fictional)")
            for n, (paper, expires, revoked) in enumerate(links):
                assignment, _ = Assignment_.objects.get_or_create(
                    contributor=contributor, paper=paper,
                    defaults={"public_id": f"a-{pid}-{n}", "relationship_to_paper": "author"})
                Invitation_.objects.create(assignment=assignment, token_hash=f"{pid}-{n}".ljust(64, "0"),
                                           expires_at=expires, revoked_at=timezone.now() if revoked else None)
            return contributor

        person("c-x", [(one, later, False), (two, later, False)])     # two working links
        person("c-y", [(one, later, False), (two, later, True)])      # the newest link is revoked
        person("c-z", [(one, past, False)])                           # only an expired link
        Contributor_.objects.create(public_id="c-w", display_name="No links (fictional)")

        executor = self.executor()
        executor.migrate(self.latest(executor))
        apps = executor.loader.project_state(self.latest(executor)).apps
        Contributor_ = apps.get_model("contributors", "Contributor")
        Invitation_ = apps.get_model("contributors", "Invitation")
        EventLog_ = apps.get_model("papers", "EventLog")
        found = {}
        for c in Contributor_.objects.all():
            current = c.current_assignment.paper.paper_id if c.current_assignment_id else None
            unrevoked = list(Invitation_.objects.filter(contributor=c, revoked_at__isnull=True).values_list("token_hash", flat=True))
            found[c.public_id] = (current, [h.rstrip("0") for h in unrevoked])
        self.assertEqual(found, {"c-x": ("p-two", ["c-x-1"]), "c-y": ("p-one", ["c-y-"]), "c-z": ("p-one", ["c-z-"]),
                                 "c-w": (None, [])})
        self.assertEqual(EventLog_.objects.filter(operation="invitation_revoked").count(), 1)

    def test_migrating_back_points_each_link_at_a_paper(self):
        executor = self.executor()
        latest = self.latest(executor)
        apps = executor.loader.project_state(latest).apps
        Paper_ = apps.get_model("papers", "Paper")
        Contributor_ = apps.get_model("contributors", "Contributor")
        Assignment_ = apps.get_model("contributors", "Assignment")
        Invitation_ = apps.get_model("contributors", "Invitation")
        one = Paper_.objects.create(paper_id="p-one", title="One", config={}, config_sha256="0" * 64)
        two = Paper_.objects.create(paper_id="p-two", title="Two", config={}, config_sha256="1" * 64)
        chooser = Contributor_.objects.create(public_id="c-v", display_name="Chooser (fictional)")
        Assignment_.objects.create(public_id="a-v1", contributor=chooser, paper=one, relationship_to_paper="author")
        chosen = Assignment_.objects.create(public_id="a-v2", contributor=chooser, paper=two,
                                            relationship_to_paper="invited_expert", added_by="contributor")
        chooser.current_assignment = chosen
        chooser.save()
        Invitation_.objects.create(contributor=chooser, token_hash="v".ljust(64, "0"), expires_at=timezone.now())
        nobody = Contributor_.objects.create(public_id="c-n", display_name="No paper (fictional)")
        Invitation_.objects.create(contributor=nobody, token_hash="n".ljust(64, "0"), expires_at=timezone.now())

        back = [("contributors", "0001_initial"), ("papers", "0002_paper_in_pool")]
        executor.migrate(back)
        apps = executor.loader.project_state(back).apps
        Invitation_ = apps.get_model("contributors", "Invitation")
        self.assertEqual(list(Invitation_.objects.values_list("assignment__public_id", flat=True)), ["a-v2"])
        executor = self.executor()
        executor.migrate(self.latest(executor))
