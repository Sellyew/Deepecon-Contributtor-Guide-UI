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
        self.assertContains(response, "has not confirmed a version")    # D-050: no confirmed version, no freeze
        self.a_emp.refresh_from_db()
        self.assertFalse(self.a_emp.is_frozen)
        selection.confirm(self.a_emp)
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


class ReviewScreenTests(SelectionTestCase):
    """The contributor's screens (MVP §3 steps 3–6, §4; plan §5 acceptance tests)."""

    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.pid = self.empirical.paper_id
        self.items = self.first_items()

    def url(self, item_id):
        return reverse("contributors:review_item", args=[self.pid, item_id])

    def post(self, item_id, fetch=False, **data):
        headers = {"HTTP_X_REQUESTED_WITH": "fetch"} if fetch else {}
        return self.client.post(self.url(item_id), data, **headers)

    def test_the_overview_shows_progress_and_the_way_in(self):
        page = self.client.get(reverse("contributors:my_paper", args=[self.pid]))
        self.assertContains(page, f"0 of {len(self.items)} reviewed")
        self.assertContains(page, reverse("contributors:review", args=[self.pid]))
        self.assertContains(page, "deliberate modifications made to build a benchmark task, not claims about the published paper")

    def test_the_review_needs_consent_and_the_current_paper(self):
        fresh = self.client_class()
        self.open_link(self.bo_token, client=fresh)              # Bo has not consented to the theory paper
        theory_item = self.first_items(self.theory)[0].item_id
        self.assertRedirects(fresh.get(reverse("contributors:review_item", args=[self.theory.paper_id, theory_item])),
                             reverse("contributors:notice", args=[self.theory.paper_id]))
        self.assertEqual(self.client.get(reverse("contributors:review_item", args=[self.theory.paper_id, theory_item])).status_code, 404)
        self.assertEqual(self.client.get(self.url("no-such-item")).status_code, 404)

    def test_the_screen_shows_the_map_the_change_and_no_scoring_material(self):
        page = self.client.get(self.url("A"))
        self.assertContains(page, "Whole picture")
        self.assertContains(page, 'class="marker colour-0 current"')
        self.assertContains(page, "keep if first_treat")             # the local change from the item map
        self.assertContains(page, "code/build/panel.do")              # shown under the author's own file name
        for forbidden in ("allowed_scores", "scoring_method", "tiers", "calibration_status"):
            self.assertNotContains(page, forbidden)
        self.assertContains(page, "review.js")

    def test_a_one_tap_answer_saves_and_moves_on(self):
        response = self.post("A", set_verdict="keep", version=0)
        self.assertRedirects(response, self.url(self.items[1].item_id))
        self.assertEqual(self.a_emp.reviews.get().verdict, "keep")
        page = self.client.get(self.url(self.items[1].item_id))
        self.assertContains(page, 'class="marker colour-0 done"')

    def test_reject_stays_and_offers_reasons(self):
        self.assertRedirects(self.post("A", set_verdict="reject", version=0), self.url("A"))
        page = self.client.get(self.url("A"))
        self.assertContains(page, "Main reason")
        self.post("A", verdict="reject", reject_reason="not_realistic", version=1, save="1")
        self.assertEqual(self.a_emp.reviews.get().reject_reason, "not_realistic")

    def test_keep_with_changes_needs_words(self):
        page = self.post("A", set_verdict="keep_with_changes", version=0)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Please say what should change")
        self.assertFalse(self.a_emp.reviews.exists())
        self.post("A", set_verdict="keep_with_changes", comment="Use the full sample.", version=0)
        self.assertEqual(self.a_emp.reviews.get().comment, "Use the full sample.")

    def test_change_then_undo_and_revisit(self):
        self.post("A", set_verdict="reject", version=0)
        self.post("A", set_verdict="keep", version=1)
        review = self.a_emp.reviews.get()
        self.assertEqual((review.verdict, review.reject_reason, review.version), ("keep", "", 2))

    def test_two_tabs_never_overwrite_silently(self):
        self.post("A", set_verdict="keep", comment="", version=0)
        stale = self.post("A", set_verdict="reject", version=0)            # the other tab still has version 0
        self.assertEqual(stale.status_code, 200)
        self.assertContains(stale, "saved from another tab or window")
        self.assertEqual(self.a_emp.reviews.get().verdict, "keep")

    def test_autosave_answers_in_json(self):
        self.post("A", set_verdict="keep", version=0)
        ok = self.post("A", fetch=True, verdict="keep", comment="Fine.", version=1, save="1")
        self.assertEqual((ok.status_code, ok.json()["version"]), (200, 2))
        self.assertEqual(self.post("A", fetch=True, verdict="keep", version=1, save="1").status_code, 409)
        bad = self.post("A", fetch=True, verdict="keep_with_changes", version=2, save="1")
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(self.a_emp.reviews.get().comment, "Fine.")

    def test_ai_disclosure_needs_the_tool_and_is_exported(self):
        page = self.post("A", set_verdict="keep", ai_used="on", version=0)
        self.assertContains(page, "Please name the tool.")
        self.post("A", set_verdict="keep", ai_used="on", ai_tool="a chat assistant", ai_account_kind="personal",
                  ai_entered_items="on", version=0)
        exported = selection.export(self.a_emp)["reviews"][0]["ai_help"]
        self.assertEqual(exported, {"used": True, "tool": "a chat assistant", "account_kind": "personal",
                                    "entered_items_or_package": True})

    def test_a_frozen_review_refuses_every_change(self):
        self.a_emp.frozen_at = timezone.now()
        self.a_emp.save()
        page = self.client.get(self.url("A"))
        self.assertContains(page, "frozen")
        self.assertContains(page, 'name="set_verdict" value="keep" class="verdict" aria-pressed="false" disabled')
        self.post("A", set_verdict="keep", version=0)
        self.assertEqual(self.post("A", fetch=True, verdict="keep", version=0, save="1").status_code, 423)
        self.client.post(reverse("contributors:propose", args=[self.pid]), {"category": "unsure", "description": "x"})
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        self.assertEqual((self.a_emp.reviews.count(), self.a_emp.proposals.count(), self.a_emp.confirmations.count()), (0, 0, 0))

    def test_proposals_can_be_added_edited_and_deleted_only_by_their_author(self):
        propose = reverse("contributors:propose", args=[self.pid])
        self.client.post(propose, {"category": "conceptual", "description": "A missed robustness check.", "location": "Table 3"})
        proposal = self.a_emp.proposals.get()
        edit = reverse("contributors:proposal_edit", args=[self.pid, proposal.public_id])
        self.client.post(edit, {"category": "unsure", "description": "Revised.", "version": "1"})
        proposal.refresh_from_db()
        self.assertEqual((proposal.category, proposal.description, proposal.version), ("unsure", "Revised.", 2))
        # A second tab still holding version 1 does not overwrite the revision.
        self.client.post(edit, {"category": "unsure", "description": "Stale tab text.", "version": "1"})
        proposal.refresh_from_db()
        self.assertEqual(proposal.description, "Revised.")
        other = self.client_class()
        self.open_link(self.bo_token, client=other)
        other.post(reverse("contributors:notice", args=[self.theory.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        self.assertEqual(other.get(reverse("contributors:proposal_edit", args=[self.theory.paper_id, proposal.public_id])).status_code, 404)
        self.client.post(edit, {"delete": "1", "version": "2"})
        self.assertFalse(self.a_emp.proposals.exists())
        self.assertEqual(list(EventLog.objects.filter(operation__startswith="proposal_").values_list("operation", flat=True)
                              .order_by("pk")), ["proposal_added", "proposal_edited", "proposal_deleted"])
        # "Save" pressed twice creates one proposal.
        for _ in range(2):
            self.client.post(propose, {"category": "conceptual", "description": "Twice.", "location": ""})
        self.assertEqual(self.a_emp.proposals.filter(description="Twice.").count(), 1)

    def test_questions_reach_the_team_and_answers_come_back(self):
        self.client.post(reverse("contributors:ask", args=[self.pid]), {"text": "Which sample?", "item_id": "A"})
        question = Question.objects.get()
        self.assertEqual(question.item.item_id, "A")
        self.assertTrue(EventLog.objects.filter(operation="question_asked").exists())
        question.answer, question.answered_at, question.answered_by = "The main sample.", timezone.now(), "team"
        question.save()
        self.assertContains(self.client.get(self.url("A")), "The main sample.")
        self.assertEqual(self.client.post(reverse("contributors:ask", args=[self.pid]), {"text": "x", "item_id": "nope"}).status_code, 404)

    def test_confirmation_shows_own_words_and_the_download_follows(self):
        self.assertEqual(self.client.get(reverse("contributors:my_review", args=[self.pid])).status_code, 404)
        self.post("A", set_verdict="keep_with_changes", comment="My own words.", version=0)
        page = self.client.get(reverse("contributors:confirm", args=[self.pid]))
        self.assertContains(page, "My own words.")
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        self.assertEqual(self.a_emp.confirmations.get().version, 1)
        download = self.client.get(reverse("contributors:my_review", args=[self.pid]))
        self.assertIn("text/markdown", download["Content-Type"])
        text = download.content.decode()
        self.assertIn("Confidential", text)
        self.assertIn("My own words.", text)

    def test_the_matrix_lists_results_against_items(self):
        page = self.client.get(reverse("contributors:review_matrix", args=[self.pid]))
        self.assertContains(page, "Results and items")
        self.assertContains(page, "●")

    def test_paired_variants_are_shown_together_and_the_choice_is_saved(self):
        item_map = self.empirical.current_rubric().item_maps.first()
        raw = item_map.raw
        first, second = self.items[0].item_id, self.items[1].item_id
        raw["items"][first]["paired_with"], raw["items"][second]["paired_with"] = second, first
        item_map.raw = raw
        item_map.save()
        page = self.client.get(self.url(first))
        self.assertContains(page, "prepared in two versions")
        self.assertContains(page, "Which version should the task keep?")
        self.post(first, set_verdict="keep", variant_choice="second", version=0)
        self.assertEqual(self.a_emp.reviews.get().variant_choice, "second")

    def test_the_review_screen_is_bilingual_but_item_text_is_not_translated(self):
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": "/"})
        page = self.client.get(self.url("A"))
        for text in ("全局视图", "修改后保留", "AI 协助了此项", "向团队提问"):
            self.assertContains(page, text)
        self.assertContains(page, "keep if first_treat")          # the item's own text stays as written
        self.assertNotContains(page, "Whole picture")

    def test_the_last_answer_leads_to_review_and_confirm(self):
        last = self.items[-1].item_id
        self.assertRedirects(self.post(last, set_verdict="unsure", version=0), reverse("contributors:confirm", args=[self.pid]))
