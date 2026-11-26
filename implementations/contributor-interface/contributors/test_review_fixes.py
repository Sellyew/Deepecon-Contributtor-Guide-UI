"""Regression tests for the findings of the M2 code review (2026-11-26).

The review was done by Claude AI agents run from a development session; each finding below was
reproduced by a second agent before it was fixed. Each test names the behaviour it protects.
"""
import io
import json
import re
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import CommandError, call_command
from django.db.models import ProtectedError
from django.urls import reverse
from django.utils import timezone

from contributors import review as selection
from contributors.models import Assignment, Confirmation, Consent, ItemReview, Question
from contributors.test_selection import SelectionTestCase
from deepecon_site.testing import example_json
from papers import importers
from papers.models import EventLog


def import_new_rubric_version(paper, version, change_rubric=None):
    """What the importer tells the team to do after changing items: a new rubric version."""
    field = "empirical" if paper.field != "theory" else "theory"
    config, rubric, item_map = (example_json(field, n) for n in ("paper-config", "rubric", "item-map"))
    if change_rubric:
        change_rubric(rubric)
    config["candidate_package_sha256"] = paper.config["candidate_package_sha256"]
    config["rubric_version"] = rubric["version"] = item_map["rubric_version"] = version
    importers.import_paper_config(json.dumps(config).encode("utf-8"), "test")
    paper.refresh_from_db()
    importers.import_rubric(paper, json.dumps(rubric).encode("utf-8"), "test")
    importers.import_item_map(paper, json.dumps(item_map).encode("utf-8"), "test")
    paper.refresh_from_db()
    return paper


class ScreenFixture(SelectionTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.pid = self.empirical.paper_id
        self.items = self.first_items()

    def url(self, item_id, paper_id=None):
        return reverse("contributors:review_item", args=[paper_id or self.pid, item_id])

    def post(self, item_id, fetch=False, **data):
        headers = {"HTTP_X_REQUESTED_WITH": "fetch"} if fetch else {}
        return self.client.post(self.url(item_id), data, **headers)

    def pair(self, first="A", second="M1"):
        item_map = self.empirical.current_rubric().item_maps.first()
        raw = item_map.raw
        raw["items"][first]["paired_with"], raw["items"][second]["paired_with"] = second, first
        item_map.raw = raw
        item_map.save()


class StaleAndConcurrentSaves(ScreenFixture):
    def test_a_stale_version_on_an_unanswered_item_is_a_conflict_not_a_crash(self):
        with self.assertRaises(selection.Conflict) as clash:
            selection.save_review(self.a_emp, self.items[0], {"verdict": "keep"}, 3)
        self.assertIsNone(clash.exception.review)
        self.assertEqual(self.post("A", fetch=True, verdict="keep", version=3, save="1").status_code, 409)
        page = self.post("A", set_verdict="keep", version=3)
        self.assertContains(page, "saved from another tab")

    def test_a_lost_race_on_the_first_save_becomes_a_conflict(self):
        item = self.items[0]
        ItemReview.objects.create(assignment=self.a_emp, item=item, verdict="keep", version=1)
        # The other request's row appears only after this one looked (possible on a server database).
        with mock.patch.object(ItemReview.objects, "select_for_update", return_value=ItemReview.objects.none()):
            with self.assertRaises(selection.Conflict) as clash:
                selection.save_review(self.a_emp, item, {"verdict": "reject"}, 0)
        self.assertEqual(clash.exception.review.verdict, "keep")

    def test_a_freeze_made_during_a_request_is_respected(self):
        stale = Assignment.objects.get(pk=self.a_emp.pk)            # loaded before the team froze it
        Assignment.objects.filter(pk=self.a_emp.pk).update(frozen_at=timezone.now(), frozen_by="team")
        with self.assertRaises(selection.Frozen):
            selection.save_review(stale, self.items[0], {"verdict": "keep"}, 0)
        with self.assertRaises(selection.Frozen):
            selection.confirm(stale)
        self.assertEqual((self.a_emp.reviews.count(), self.a_emp.confirmations.count()), (0, 0))

    def test_sqlite_write_transactions_begin_immediately(self):
        from django.conf import settings
        self.assertEqual(settings.DATABASES["default"]["OPTIONS"].get("transaction_mode"), "IMMEDIATE")


class RubricVersions(ScreenFixture):
    def test_answers_belong_to_the_rubric_version_they_were_given_on(self):
        self.post("A", set_verdict="reject", version=0)
        self.post("A", save="1", verdict="reject", reject_reason="not_realistic", comment="Too far-fetched.", version=1)
        import_new_rubric_version(self.empirical, "example_rubric_2")
        self.a_emp.refresh_from_db()
        self.assertEqual(selection.progress(self.a_emp)["reviewed"], 0)
        self.assertEqual(selection.reviews_by_item(self.a_emp), {})
        page = self.client.get(self.url("A"))
        self.assertContains(page, "Your answer to the earlier version was: Reject")
        self.assertContains(page, "Too far-fetched.")
        self.assertContains(page, 'name="version" value="0"')
        self.assertRedirects(self.client.get(reverse("contributors:review", args=[self.pid])), self.url("A"))
        self.assertEqual(self.post("A", set_verdict="keep", version=0).status_code, 302)
        data = selection.export(self.a_emp)
        self.assertEqual(data["rubric_version"], "example_rubric_2")
        ids = [r["item_id"] for r in data["reviews"]]
        self.assertEqual(sorted(ids), sorted(set(ids)))              # each item once
        self.assertEqual(next(r for r in data["reviews"] if r["item_id"] == "A")["verdict"], "keep")
        self.make_freezable()
        _, warnings = selection.freeze_problems(self.a_emp)
        self.assertTrue(any("earlier rubric version" in w for w in warnings))


class WhatContributorsSee(SelectionTestCase):
    def setUp(self):
        super().setUp()
        self.open_link(self.bo_token)
        self.consent(self.theory)
        self.client.post(reverse("set_language"), {"language": "en", "next": "/"})   # Bo's preset is Chinese

    def test_hidden_affected_results_stay_off_the_map_and_the_matrix(self):
        the_map = selection.map_for(self.b_th)
        p2 = next(n for n in the_map["nodes"] if n["id"] == "p2")
        self.assertEqual({m["item_id"] for m in p2["affected_by"]}, {"D1", "S1"})   # proof-gap hides affected_results
        page = self.client.get(reverse("contributors:review_item", args=[self.theory.paper_id, "G1"]))
        results = re.search(r'<ul class="results">(.*?)</ul>', page.content.decode(), re.S).group(1)
        self.assertNotIn(">G1<", results)
        self.assertNotContains(page, "Affects")
        matrix = self.client.get(reverse("contributors:review_matrix", args=[self.theory.paper_id]))
        columns = [c["id"] for c in matrix.context["columns"]]
        for row in matrix.context["rows"]:
            self.assertFalse(row["cells"][columns.index("G1")])

    def test_no_weight_or_scoring_values_on_any_page(self):
        selection.save_review(self.b_th, self.first_items(self.theory)[0], {"verdict": "keep"}, 0)
        selection.confirm(self.b_th)
        pid = self.theory.paper_id
        for name, args in (("review_item", [pid, "G1"]), ("review_item", [pid, "D1"]), ("confirm", [pid]),
                           ("my_review", [pid]), ("review_matrix", [pid])):
            page = self.client.get(reverse(f"contributors:{name}", args=args))
            self.assertEqual(page.status_code, 200)
            for hidden in ("Weight:", "allowed_scores", "tiers", "calibration_status"):
                self.assertNotContains(page, hidden)

    def test_paper_passages_show_their_locator_and_never_none(self):
        page = self.client.get(reverse("contributors:review_item", args=[self.theory.paper_id, "D1"]))
        self.assertContains(page, "Appendix A, eq. (A.7)")
        self.assertNotContains(page, '<p class="path">None')

    def test_selecting_a_result_highlights_the_items_that_affect_it(self):
        the_map = selection.map_for(self.b_th, result="p2")
        markers = {m["item_id"]: m for n in the_map["nodes"] for m in n["affected_by"] + n["items_here"]}
        self.assertTrue(markers["D1"]["highlight"] and markers["S1"]["highlight"])
        self.assertFalse(markers["G1"]["highlight"])                               # its link to p2 is hidden
        page = self.client.get(reverse("contributors:review_item", args=[self.theory.paper_id, "D1"]) + "?result=p2")
        self.assertContains(page, "highlight")
        self.assertContains(page, "Clear the highlight")


class TheReviewForm(ScreenFixture):
    def test_enter_in_a_text_field_saves_and_never_changes_the_answer(self):
        page = self.client.get(self.url("A")).content.decode()
        form = page[page.index('id="review-form"'):]
        self.assertLess(form.index('name="save"'), form.index('name="set_verdict"'))    # the default button
        self.post("A", set_verdict="reject", version=0)
        # What the browser sends for Enter: the default button, i.e. save=1, and the hidden verdict.
        response = self.post("A", save="1", verdict="reject", reject_reason="not_realistic",
                             suggested_title="A clearer title", version=1)
        self.assertRedirects(response, self.url("A"))
        review = self.a_emp.reviews.get()
        self.assertEqual((review.verdict, review.reject_reason), ("reject", "not_realistic"))

    def test_the_chosen_answer_is_announced_and_the_reason_is_labelled(self):
        self.post("A", set_verdict="reject", version=0)
        page = self.client.get(self.url("A"))
        self.assertContains(page, 'value="reject" class="verdict chosen" aria-pressed="true"')
        self.assertContains(page, '<label for="id_reject_reason">')

    def test_paired_markers_are_not_styled_as_the_pair_card_grid(self):
        self.pair("A", "M1")
        page = self.client.get(self.url("A")).content.decode()
        self.assertIn("marker-paired", page)
        self.assertNotRegex(page, r'class="marker[^"]* paired[ "]')        # .paired is the side-by-side card grid

    def test_an_invalid_post_keeps_the_partner_version_the_page_was_loaded_with(self):
        self.pair("A", "M1")
        stale = self.client.get(self.url("M1")).context["partner_version"]          # 0: A not answered yet
        self.post("A", set_verdict="keep", variant_choice="second", version=0, partner_version=0)
        invalid = self.post("M1", set_verdict="keep_with_changes", variant_choice="", version=0, partner_version=stale)
        self.assertEqual(int(invalid.context["partner_version"]), stale)      # not refreshed behind the stale choice
        again = self.post("M1", fetch=True, save="1", verdict="keep", variant_choice="", version=0,
                          partner_version=invalid.context["partner_version"])
        self.assertEqual(again.status_code, 409)
        self.assertEqual(self.a_emp.reviews.get(item__item_id="A").variant_choice, "second")

    def test_paired_versions_keep_one_order_and_one_answer(self):
        self.pair("A", "M1")
        for item_id in ("A", "M1"):
            page = self.client.get(self.url(item_id))
            self.assertEqual([c["card"]["id"] for c in page.context["pair_cards"]], ["A", "M1"])
        self.post("A", set_verdict="keep", variant_choice="second", version=0)
        page = self.client.get(self.url("M1"))
        self.assertEqual(page.context["form"].initial.get("variant_choice"), "second")   # the pair's answer
        self.post("M1", set_verdict="keep", variant_choice="second", version=0, partner_version=1)
        self.post("A", save="1", verdict="keep", variant_choice="first", version=1, partner_version=1)
        choices = dict(self.a_emp.reviews.values_list("item__item_id", "variant_choice"))
        self.assertEqual(choices, {"A": "first", "M1": "first"})
        self.assertEqual(self.a_emp.reviews.get(item__item_id="M1").version, 2)

    def test_a_stale_page_of_one_paired_item_cannot_erase_the_choice_made_on_the_other(self):
        self.pair("A", "M1")
        stale_m1 = self.client.get(self.url("M1")).context["partner_version"]       # loaded before A is answered
        self.assertEqual(stale_m1, 0)
        response = self.post("A", fetch=True, save="1", verdict="keep", variant_choice="second", version=0, partner_version=0)
        self.assertEqual(response.json()["partner_version"], 0)
        response = self.post("M1", fetch=True, save="1", verdict="keep", variant_choice="", version=0, partner_version=stale_m1)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.a_emp.reviews.get(item__item_id="A").variant_choice, "second")
        page = self.post("M1", set_verdict="keep", variant_choice="", version=0, partner_version=stale_m1)
        self.assertContains(page, "saved from another tab")
        self.assertEqual(page.context["form"].initial["variant_choice"], "second")
        # The same page after a reload carries the partner's version and may change the pair's answer.
        fresh = self.client.get(self.url("M1")).context["partner_version"]
        self.post("M1", set_verdict="keep", variant_choice="both", version=0, partner_version=fresh)
        self.assertEqual(set(self.a_emp.reviews.values_list("variant_choice", flat=True)), {"both"})


class ConfirmationAndDownload(ScreenFixture):
    def test_the_export_language_is_the_one_the_contributor_used(self):
        self.post("A", set_verdict="keep", version=0)
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": "/"})
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        self.assertEqual(self.a_emp.confirmations.get().language, "zh-Hans")
        self.assertEqual(selection.export(self.a_emp)["language"], "zh-Hans")

    def test_a_double_submitted_edit_is_not_a_conflict_and_similar_proposals_are_kept(self):
        propose = reverse("contributors:propose", args=[self.pid])
        self.client.post(propose, {"category": "conceptual", "description": "Same words.", "why_it_matters": "One."})
        proposal = self.a_emp.proposals.get()
        edit = reverse("contributors:proposal_edit", args=[self.pid, proposal.public_id])
        data = {"category": "conceptual", "description": "Edited.", "why_it_matters": "One.", "version": "1"}
        self.client.post(edit, data)
        second = self.client.post(edit, data, follow=True)              # the second press of "Save"
        self.assertNotContains(second, "changed in another tab")
        self.assertContains(second, "Your proposal was saved.")
        # A different proposal that shares only category and description is not a duplicate.
        self.client.post(propose, {"category": "conceptual", "description": "Edited.", "why_it_matters": "Two."})
        self.assertEqual(self.a_emp.proposals.count(), 2)

    def test_the_download_uses_the_interface_language_for_labels(self):
        self.post("A", set_verdict="reject", version=0)
        self.post("A", save="1", verdict="reject", reject_reason="not_realistic", suggested_title="Better", version=1)
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        text = self.client.get(reverse("contributors:my_review", args=[self.pid])).content.decode()
        self.assertIn("Main reason: Not realistic", text)
        self.assertIn("Suggested title: Better", text)
        self.assertNotIn("not_realistic", text)
        self.assertNotIn("reject reason", text)
        self.assertIn("(Conceptual error)", text)


class ScoringMaterialStaysHidden(ScreenFixture):
    """Scoring material and the roles a configuration hides never reach a contributor page,
    checked by their values (distinctive markers), not by key names."""

    def pages(self):
        self.post("A", set_verdict="keep", version=0)
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        return [self.url(i.item_id) for i in self.first_items()] + [
            reverse(f"contributors:{name}", args=[self.pid])
            for name in ("my_paper", "review_matrix", "propose", "confirm", "my_review")]

    def assert_absent(self, markers):
        for url in self.pages():
            page = self.client.get(url)
            self.assertEqual(page.status_code, 200)
            for marker in markers:
                with self.subTest(url=url, marker=marker):
                    self.assertNotContains(page, marker)

    def test_tiers_scoring_method_calibration_and_scores_never_reach_a_page(self):
        def mark(rubric):
            rubric["calibration_status"] = "CALIBRATION-MARK"
            total = 0
            for group in ("conceptual", "missing", "technical"):
                for item in rubric[group]:
                    # Distinctive scores that still pass the import checks (points = the largest score,
                    # tier keys = the allowed scores, the maximum = the sum of points).
                    item["allowed_scores"], item["points"] = [0, 7777], 7777
                    item["tiers"] = {"0": "TIER-TEXT-0", "7777": "TIER-TEXT-7777"}
                    item["scoring_method"] = f"SCORING-METHOD-{item['id']}"
                    total += 7777
            rubric["maximum"] = total
        import_new_rubric_version(self.empirical, "example_rubric_marked", change_rubric=mark)
        self.assertIn("SCORING-METHOD-", json.dumps(self.empirical.current_rubric().raw))   # the markers are stored
        self.assert_absent(["TIER-TEXT-", "SCORING-METHOD-", "CALIBRATION-MARK", "7777", "23331", "Weight:"])

    def test_roles_a_category_hides_never_reach_a_page(self):
        config = example_json("empirical", "paper-config")
        config["candidate_package_sha256"] = self.empirical.config["candidate_package_sha256"]
        missing = next(c for c in config["categories"] if c["id"] == "missing")
        missing["visible_roles"] = [r for r in missing["visible_roles"] if r not in ("description", "acceptable_answer")]
        importers.import_paper_config(json.dumps(config).encode("utf-8"), "test")
        rubric = self.empirical.current_rubric()
        raw = rubric.raw
        for item in raw["missing"]:
            item["available_evidence_and_boundary"] = "HIDDEN-DESCRIPTION-MARK"
            item["acceptable_work"] = "HIDDEN-ACCEPTABLE-MARK"
        config["rubric_version"] = raw["version"] = "example_rubric_hidden_roles"
        importers.import_paper_config(json.dumps(config).encode("utf-8"), "test")
        self.empirical.refresh_from_db()
        importers.import_rubric(self.empirical, json.dumps(raw).encode("utf-8"), "test")
        item_map = example_json("empirical", "item-map")
        item_map["rubric_version"] = raw["version"]
        importers.import_item_map(self.empirical, json.dumps(item_map).encode("utf-8"), "test")
        self.empirical.refresh_from_db()
        self.assertEqual([it.category for it in self.first_items() if it.item_id == "M1"], ["missing"])
        self.assert_absent(["HIDDEN-DESCRIPTION-MARK", "HIDDEN-ACCEPTABLE-MARK"])


class EndpointsAreGated(ScreenFixture):
    """Plan §3: guessed IDs, copied URLs, and other papers are refused on every Selection endpoint."""

    ENDPOINTS = [("review", [], "get"), ("review_matrix", [], "get"), ("propose", [], "get"), ("propose", [], "post"),
                 ("ask", [], "post"), ("confirm", [], "get"), ("confirm", [], "post"), ("my_review", [], "get"),
                 ("review_item", ["A"], "get"), ("review_item", ["A"], "post")]

    def call(self, name, paper_id, extra, method):
        url = reverse(f"contributors:{name}", args=[paper_id, *extra])
        return getattr(self.client, method)(url, {"text": "x", "description": "x", "category": "unsure"} if method == "post" else {})

    def test_other_papers_and_unknown_papers_are_not_found(self):
        for name, extra, method in self.ENDPOINTS:
            for paper_id in (self.theory.paper_id, "no-such-paper"):
                with self.subTest(name=name, method=method, paper=paper_id):
                    self.assertEqual(self.call(name, paper_id, extra, method).status_code, 404)

    def test_an_offered_paper_that_is_not_current_must_be_chosen_first(self):
        self.assign(self.alice, self.theory, relationship="invited_expert", current=False)
        for name, extra, method in self.ENDPOINTS:
            with self.subTest(name=name, method=method):
                response = self.call(name, self.theory.paper_id, extra, method)
                self.assertRedirects(response, reverse("contributors:choose", args=[self.theory.paper_id]),
                                     fetch_redirect_response=False)

    def test_nothing_works_without_consent(self):
        Consent.objects.filter(assignment=self.a_emp).delete()
        for name, extra, method in self.ENDPOINTS:
            with self.subTest(name=name, method=method):
                response = self.call(name, self.pid, extra, method)
                self.assertRedirects(response, reverse("contributors:notice", args=[self.pid]), fetch_redirect_response=False)
        self.assertEqual((self.a_emp.reviews.count(), self.a_emp.proposals.count(), Question.objects.count()), (0, 0, 0))


class TeamPages(SelectionTestCase):
    def setUp(self):
        super().setUp()
        self.team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(self.team)
        self.changelist = reverse("admin:contributors_assignment_changelist")
        self.review = selection.save_review(self.a_emp, self.first_items()[0], {"verdict": "keep"}, 0)
        self.version = selection.confirm(self.a_emp)

    def test_contributors_records_cannot_be_deleted_on_the_team_pages(self):
        question = Question.objects.create(assignment=self.a_emp, text="Why?")
        self.client.logout()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        self.client.force_login(self.team)
        for model, obj in (("itemreview", self.review), ("confirmation", self.version), ("question", question),
                           ("consent", Consent.objects.filter(assignment=self.a_emp).first())):
            with self.subTest(model=model):
                url = reverse(f"admin:contributors_{model}_delete", args=[obj.pk])
                self.assertEqual(self.client.post(url, {"post": "yes"}).status_code, 403)
        self.assertEqual((ItemReview.objects.count(), Confirmation.objects.count(), Question.objects.count()), (1, 1, 1))

    def test_an_assignment_with_work_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.a_emp.delete()
        page = self.client.post(reverse("admin:contributors_assignment_delete", args=[self.a_emp.pk]), {"post": "yes"})
        self.assertContains(page, "Cannot delete")
        self.assertTrue(Assignment.objects.filter(pk=self.a_emp.pk).exists())

    def test_freezing_records_what_was_frozen_and_warns_about_later_changes(self):
        self.make_freezable()
        selection.save_review(self.a_emp, self.first_items()[0], {"verdict": "reject"}, 1)   # after version 1
        response = self.client.post(self.changelist, {"action": "freeze", "_selected_action": [self.a_emp.pk]}, follow=True)
        self.assertContains(response, "changed after version 1 was confirmed")
        event = EventLog.objects.get(operation="review_frozen")
        self.assertEqual(event.details["confirmation_version"], 1)
        self.assertFalse(event.details["matches_confirmation"])
        self.assertEqual(event.details["content_sha256"], selection.content_sha256(selection.snapshot(self.a_emp)))

    def test_the_export_needs_permission_to_view_the_contributors_records(self):
        viewer = get_user_model().objects.create_user("viewer", "v@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.add(Permission.objects.get(codename="view_assignment"))
        self.client.force_login(viewer)
        response = self.client.post(self.changelist, {"action": "export_review", "_selected_action": [self.a_emp.pk]})
        self.assertNotIn("Content-Disposition", response)
        for codename in ("view_itemreview", "view_proposal", "view_question", "view_consent", "view_confirmation"):
            viewer.user_permissions.add(Permission.objects.get(codename=codename))
        viewer = get_user_model().objects.get(pk=viewer.pk)
        self.client.force_login(viewer)
        response = self.client.post(self.changelist, {"action": "export_review", "_selected_action": [self.a_emp.pk]})
        self.assertIn("attachment", response["Content-Disposition"])

    def test_removing_an_answer_puts_the_question_back_in_the_queue(self):
        question = Question.objects.create(assignment=self.a_emp, text="Which sample?")
        change = reverse("admin:contributors_question_change", args=[question.pk])
        self.client.post(change, {"answer": ""})
        self.assertFalse(EventLog.objects.filter(operation="question_answered").exists())
        self.client.post(change, {"answer": "The main sample."})
        question.refresh_from_db()
        self.assertIsNotNone(question.answered_at)
        self.client.post(change, {"answer": ""})
        question.refresh_from_db()
        self.assertEqual((question.answer, question.answered_at, question.answered_by), ("", None, ""))
        self.assertEqual(Question.objects.filter(answered_at__isnull=True).first(), question)
        self.assertTrue(EventLog.objects.filter(operation="question_answer_removed").exists())


class Withdrawal(SelectionTestCase):
    """The notice: "You may withdraw at any time by telling the team; your reviews, proposals,
    and uploads are then deleted." Plan §3: a logged administrator action."""

    def setUp(self):
        super().setUp()
        self.open_link(self.alice_token)
        self.consent(self.empirical)
        selection.save_review(self.a_emp, self.first_items()[0], {"verdict": "keep", "comment": "private words"}, 0)
        selection.confirm(self.a_emp)
        Question.objects.create(assignment=self.a_emp, text="Which sample?")
        self.team = get_user_model().objects.create_superuser("team", "team@example.org", "a-long-test-password")
        self.client.force_login(self.team)
        self.url = reverse("admin:contributors_assignment_withdraw", args=[self.a_emp.pk])

    def test_three_steps_delete_the_work_and_log_counts_only(self):
        self.assertContains(self.client.get(reverse("admin:contributors_assignment_change", args=[self.a_emp.pk])), "Withdraw…")
        self.assertContains(self.client.get(self.url), "has asked to withdraw")
        self.assertContains(self.client.get(self.url, {"step": "2"}), "cannot be undone")
        today = timezone.localdate().isoformat()
        wrong = self.client.post(self.url, {"step": "3", "requested_on": today, "request_channel": "email", "confirmation": "a-wrong"})
        self.assertContains(wrong, "exactly to confirm")
        self.assertTrue(Assignment.objects.filter(pk=self.a_emp.pk).exists())
        self.client.post(self.url, {"step": "3", "requested_on": today, "request_channel": "email",
                                    "confirmation": self.a_emp.public_id})
        self.assertFalse(Assignment.objects.filter(pk=self.a_emp.pk).exists())
        self.assertEqual((ItemReview.objects.count(), Confirmation.objects.count(), Question.objects.count(),
                          Consent.objects.filter(assignment_id=self.a_emp.pk).count()), (0, 0, 0, 0))
        self.alice.refresh_from_db()
        self.assertIsNone(self.alice.current_assignment)
        event = EventLog.objects.get(operation="withdrawn_on_request")
        self.assertEqual((event.details["reviews_deleted"], event.details["questions_deleted"]), (1, 1))
        self.assertNotIn("private words", json.dumps(event.details))

    def test_a_team_member_who_cannot_see_contributors_lands_on_the_index(self):
        member = get_user_model().objects.create_user("member", "m@example.org", "a-long-test-password", is_staff=True)
        member.user_permissions.add(*Permission.objects.filter(codename__in=["view_assignment", "delete_assignment"]))
        self.client.force_login(member)
        response = self.client.post(self.url, {"step": "3", "requested_on": timezone.localdate().isoformat(),
                                               "request_channel": "email", "confirmation": self.a_emp.public_id})
        self.assertRedirects(response, reverse("admin:index"))
        self.assertFalse(Assignment.objects.filter(pk=self.a_emp.pk).exists())

    def test_a_consent_page_offers_no_delete_button(self):
        consent = Consent.objects.filter(assignment=self.a_emp).first()
        page = self.client.get(reverse("admin:contributors_consent_change", args=[consent.pk]))
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "deletelink")

    def test_withdrawal_needs_the_delete_permission(self):
        viewer = get_user_model().objects.create_user("viewer", "v@example.org", "a-long-test-password", is_staff=True)
        viewer.user_permissions.add(Permission.objects.get(codename="change_assignment"))
        self.client.force_login(viewer)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_an_assignment_with_consent_but_no_work_can_still_be_deleted(self):
        b_emp = self.assign(self.bo, self.empirical, current=False)
        bo = self.client_class()
        self.open_link(self.bo_token, client=bo)
        bo.post(reverse("contributors:choose", args=[self.empirical.paper_id]), {"confirm": "1"})
        bo.post(reverse("contributors:notice", args=[self.empirical.paper_id]), {"acknowledge_evaluation": "on", "team_ai_use": "no"})
        self.assertTrue(Consent.objects.filter(assignment=b_emp).exists())
        self.client.post(reverse("admin:contributors_assignment_delete", args=[b_emp.pk]), {"post": "yes"})
        self.assertFalse(Assignment.objects.filter(pk=b_emp.pk).exists())


class CheckPapersRechecksEverything(SelectionTestCase):
    def setUp(self):
        super().setUp()
        self.make_freezable(self.empirical)
        self.make_freezable(self.theory)

    def run_check(self):
        out = io.StringIO()
        with self.assertRaises(CommandError):
            call_command("check_papers", stdout=out)
        return out.getvalue()

    def test_a_stored_item_map_that_todays_schema_refuses_fails(self):
        item_map = self.empirical.current_rubric().item_maps.first()
        item_map.raw = {**item_map.raw, "unexpected": True}
        item_map.save()
        self.assertIn("item-map", self.run_check())

    def test_a_stored_rubric_that_todays_schema_refuses_fails(self):
        rubric = self.empirical.current_rubric()
        rubric.raw = {**rubric.raw, "version": 7}
        rubric.save()
        self.assertIn("rubric-import", self.run_check())

    def test_an_item_map_for_another_paper_fails(self):
        item_map = self.empirical.current_rubric().item_maps.first()
        item_map.raw = {**item_map.raw, "paper_id": self.theory.paper_id}
        item_map.save()
        self.assertIn(f"item map is for paper {self.theory.paper_id}", self.run_check())
