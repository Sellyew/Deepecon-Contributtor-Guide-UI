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


def import_new_rubric_version(paper, version):
    """What the importer tells the team to do after changing items: a new rubric version."""
    field = "empirical" if paper.field != "theory" else "theory"
    config, rubric, item_map = (example_json(field, n) for n in ("paper-config", "rubric", "item-map"))
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

    def test_paired_versions_keep_one_order_and_one_answer(self):
        self.pair("A", "M1")
        for item_id in ("A", "M1"):
            page = self.client.get(self.url(item_id))
            self.assertEqual([c["card"]["id"] for c in page.context["pair_cards"]], ["A", "M1"])
        self.post("A", set_verdict="keep", variant_choice="second", version=0)
        page = self.client.get(self.url("M1"))
        self.assertEqual(page.context["form"].initial.get("variant_choice"), "second")   # the pair's answer
        self.post("M1", set_verdict="keep", variant_choice="second", version=0)
        self.post("A", save="1", verdict="keep", variant_choice="first", version=1)
        choices = dict(self.a_emp.reviews.values_list("item__item_id", "variant_choice"))
        self.assertEqual(choices, {"A": "first", "M1": "first"})
        self.assertEqual(self.a_emp.reviews.get(item__item_id="M1").version, 2)


class ConfirmationAndDownload(ScreenFixture):
    def test_the_export_language_is_the_one_the_contributor_used(self):
        self.post("A", set_verdict="keep", version=0)
        self.client.post(reverse("set_language"), {"language": "zh-hans", "next": "/"})
        self.client.post(reverse("contributors:confirm", args=[self.pid]))
        self.assertEqual(self.a_emp.confirmations.get().language, "zh-Hans")
        self.assertEqual(selection.export(self.a_emp)["language"], "zh-Hans")

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
