"""M2 Selection: review rules, confirmations, export, freezing, and the team's tools (plan §2.3–2.7; D-049)."""
import io
import json
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command
from django.urls import reverse
from django.utils import timezone

from contributors import review as selection
from contributors.models import Question
from contributors.tests import ContributorSiteTestCase
from papers.models import EventLog, Item


class SelectionTestCase(ContributorSiteTestCase):
    def item(self, item_id, paper=None):
        return Item.objects.get(rubric=(paper or self.empirical).current_rubric(), item_id=item_id)

    def first_items(self, paper=None):
        return selection.paper_items(paper or self.empirical)

    def make_freezable(self, paper=None):
        paper = paper or self.empirical
        paper.built_on = date(2026, 11, 20)
        paper.save()
        Item.objects.filter(rubric=paper.current_rubric(), origin__isnull=True).update(
            origin={"drafted_by": "team", "ai_reviewed": False})


class ReviewRuleTests(SelectionTestCase):
    def test_a_save_increments_the_version(self):
        item = self.first_items()[0]
        review = selection.save_review(self.a_emp, item, {"verdict": "keep"}, 0)
        self.assertEqual(review.version, 1)
        review = selection.save_review(self.a_emp, item, {"verdict": "unsure"}, 1)
        self.assertEqual((review.version, review.verdict), (2, "unsure"))

    def test_a_stale_page_is_refused_not_overwritten(self):
        item = self.first_items()[0]
        selection.save_review(self.a_emp, item, {"verdict": "keep", "comment": "first tab"}, 0)
        with self.assertRaises(selection.Conflict) as conflict:
            selection.save_review(self.a_emp, item, {"verdict": "reject"}, 0)      # second tab, loaded before
        self.assertEqual(conflict.exception.review.comment, "first tab")
        self.assertEqual(self.a_emp.reviews.get().verdict, "keep")

    def test_reject_reason_and_ai_details_are_cleared_when_they_no_longer_apply(self):
        item = self.first_items()[0]
        selection.save_review(self.a_emp, item, {"verdict": "reject", "reject_reason": "not_realistic", "ai_used": True,
                                                 "ai_tool": "a chat assistant", "ai_entered_items": True}, 0)
        review = selection.save_review(self.a_emp, item, {"verdict": "keep", "ai_used": False}, 1)
        self.assertEqual((review.reject_reason, review.ai_tool, review.ai_entered_items), ("", "", None))

    def test_a_frozen_review_cannot_change(self):
        self.a_emp.frozen_at = timezone.now()
        self.a_emp.save()
        with self.assertRaises(selection.Frozen):
            selection.save_review(self.a_emp, self.first_items()[0], {"verdict": "keep"}, 0)
        with self.assertRaises(selection.Frozen):
            selection.confirm(self.a_emp)

    def test_progress_counts_unsure_as_reviewed(self):
        items = self.first_items()
        selection.save_review(self.a_emp, items[0], {"verdict": "unsure"}, 0)
        p = selection.progress(self.a_emp)
        self.assertEqual((p["reviewed"], p["total"]), (1, len(items)))


class ConfirmationAndExportTests(SelectionTestCase):
    def test_confirmations_are_numbered_and_hashed(self):
        item = self.first_items()[0]
        selection.save_review(self.a_emp, item, {"verdict": "keep"}, 0)
        first = selection.confirm(self.a_emp)
        selection.save_review(self.a_emp, item, {"verdict": "unsure"}, 1)
        second = selection.confirm(self.a_emp)
        self.assertEqual((first.version, second.version), (1, 2))
        self.assertEqual(first.content_sha256, selection.content_sha256(first.content))
        self.assertNotEqual(first.content_sha256, second.content_sha256)
        self.assertEqual(first.content["reviews"][0]["verdict"], "keep")      # the snapshot keeps what was confirmed

    def test_export_validates_against_the_schema(self):
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        items = self.first_items()
        selection.save_review(self.a_emp, items[0], {"verdict": "keep_with_changes", "comment": "Say why.",
                                                     "check_realistic": "yes", "ai_used": True, "ai_tool": "a tool",
                                                     "ai_account_kind": "work", "ai_entered_items": False}, 0)
        self.a_emp.proposals.create(category="unsure", description="Another error.", location="Table 2")
        Question.objects.create(assignment=self.a_emp, item=items[0], text="What is meant here?", answer="This.",
                                answered_at=timezone.now(), answered_by="team")
        selection.confirm(self.a_emp)
        data = selection.export(self.a_emp)        # raises if it fails the schema
        self.assertEqual(len(data["reviews"]), len(items))
        self.assertEqual({r["verdict"] for r in data["reviews"][1:]}, {"not_reviewed"})
        self.assertEqual([m["author"] for m in data["messages"]], ["contributor", "team"])
        self.assertTrue(data["consent"]["evaluation_through_apis_acknowledged"])
        self.assertEqual(data["reviews"][0]["ai_help"]["account_kind"], "work")


class FreezeAndAdminTests(SelectionTestCase):
    def setUp(self):
        super().setUp()
        self.team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(self.team)
        self.changelist = reverse("admin:contributors_assignment_changelist")

    def act(self, action):
        return self.client.post(self.changelist, {"action": action, "_selected_action": [self.a_emp.pk]}, follow=True)

    def test_freezing_needs_a_build_date_and_provenance(self):
        response = self.act("freeze")
        self.assertContains(response, "no task build date")
        self.assertContains(response, "items without provenance")
        self.a_emp.refresh_from_db()
        self.assertFalse(self.a_emp.is_frozen)
        self.make_freezable()
        response = self.act("freeze")
        self.assertContains(response, "not answered")                   # a warning, not a block
        self.a_emp.refresh_from_db()
        self.assertTrue(self.a_emp.is_frozen)
        self.assertTrue(EventLog.objects.filter(operation="review_frozen").exists())
        self.act("unfreeze")
        self.a_emp.refresh_from_db()
        self.assertFalse(self.a_emp.is_frozen)

    def test_export_action_downloads_valid_json(self):
        selection.save_review(self.a_emp, self.first_items()[0], {"verdict": "keep"}, 0)
        response = self.client.post(self.changelist, {"action": "export_review", "_selected_action": [self.a_emp.pk]})
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        data = json.loads(response.content)
        self.assertEqual(data["assignment_id"], self.a_emp.public_id)

    def test_question_queue_lists_unanswered_first_and_records_the_answer(self):
        items = self.first_items()
        old = Question.objects.create(assignment=self.a_emp, item=items[0], text="Old question")
        Question.objects.filter(pk=old.pk).update(created_at=timezone.now() - timezone.timedelta(days=3))
        answered = Question.objects.create(assignment=self.a_emp, text="Answered", answer="Yes.",
                                           answered_at=timezone.now(), answered_by="team")
        newer = Question.objects.create(assignment=self.a_emp, text="New question")
        self.assertEqual(list(Question.objects.all()), [old, newer, answered])
        page = self.client.get(reverse("admin:contributors_question_changelist"))
        self.assertContains(page, "3 day(s)")
        self.client.post(reverse("admin:contributors_question_change", args=[newer.pk]), {"answer": "Here is the answer."})
        newer.refresh_from_db()
        self.assertEqual(newer.answered_by, "team")
        self.assertIsNotNone(newer.answered_at)

    def test_build_date_and_owner_are_set_on_the_paper_page(self):
        response = self.client.post(reverse("admin:papers_paper_change", args=[self.empirical.pk]),
                                    {"built_on": "2026-11-20", "team_owner": self.team.pk})
        self.assertEqual(response.status_code, 302)
        self.empirical.refresh_from_db()
        self.assertEqual((self.empirical.built_on, self.empirical.team_owner), (date(2026, 11, 20), self.team))
        self.assertTrue(EventLog.objects.filter(operation="build_date_set").exists())


class CheckPapersTests(SelectionTestCase):
    def test_reports_missing_build_dates_and_provenance(self):
        out = io.StringIO()
        with self.assertRaises(CommandError):
            call_command("check_papers", stdout=out)
        self.assertIn("no task build date", out.getvalue())
        self.assertIn("items without provenance", out.getvalue())

    def test_passes_when_every_paper_is_complete(self):
        self.make_freezable(self.empirical)
        self.make_freezable(self.theory)
        out = io.StringIO()
        call_command("check_papers", stdout=out)
        self.assertIn(f"{self.empirical.paper_id}: ok", out.getvalue())

    def test_detects_a_changed_package_file(self):
        self.make_freezable(self.empirical)
        self.make_freezable(self.theory)
        from papers.importers import package_path
        with open(package_path(self.empirical.current_package()), "ab") as handle:
            handle.write(b"tampered")
        out = io.StringIO()
        with self.assertRaises(CommandError):
            call_command("check_papers", stdout=out)
        self.assertIn("no longer matches its SHA-256", out.getvalue())
