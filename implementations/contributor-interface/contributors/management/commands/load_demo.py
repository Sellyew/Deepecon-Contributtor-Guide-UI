"""Load the fictional examples for the Stage 0 demo (M1 runs with synthetic examples only)."""
import hashlib
import io
import json
import zipfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from contributors.models import Assignment, Contributor, issue_invitation
from papers import importers

ACTOR = "load_demo"
FIELDS = ("empirical", "theory")


def synthetic_package(paper_id):
    """A small, deterministic ZIP standing in for an agent-facing package. No real code or data."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, text in [
            ("README.txt", f"FICTIONAL EXAMPLE: synthetic candidate package for {paper_id}. It contains no real code or data.\n"),
            ("02_code/example_main.do", "* FICTIONAL EXAMPLE: placeholder script\n"),
        ]:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, text)
    return buf.getvalue()


def load_examples():
    examples = Path(settings.SCHEMA_DIR) / "examples"
    papers = {}
    for field in FIELDS:
        config = json.loads((examples / field / "paper-config.json").read_text(encoding="utf-8"))
        package = synthetic_package(config["paper_id"])
        config["candidate_package_sha256"] = hashlib.sha256(package).hexdigest()
        paper = importers.import_paper_config(json.dumps(config).encode("utf-8"), ACTOR)
        importers.import_rubric(paper, examples / field / "rubric.json", ACTOR)
        importers.import_item_map(paper, examples / field / "item-map.json", ACTOR)
        importers.import_candidate_package(paper, io.BytesIO(package), ACTOR)
        papers[field] = paper
    return papers


class Command(BaseCommand):
    help = ("Import the fictional empirical (scored) and theory (demo) examples, open the demo paper to all contributors, "
            "create three demo contributors (two authors with their paper set, one invited expert who chooses), and print "
            "their links. Stage 0 only.")

    def add_arguments(self, parser):
        parser.add_argument("--no-invitations", action="store_true")

    def handle(self, no_invitations=False, **options):
        if settings.STAGE != "0":
            raise CommandError("load_demo is for the Stage 0 demo computer only.")
        try:
            papers = load_examples()
        except importers.ImportRefused as refused:
            for problem in refused.problems:
                self.stderr.write(f"  - {problem}")
            raise CommandError("The examples could not be imported.")
        # Only demo or development papers can be open to all (D-047): the theory example is a demo
        # task; the empirical example is a (fictional) scored task, offered by invitation only.
        for paper in papers.values():
            if paper.publication_status == paper.DEMO:
                paper.in_pool = True
                paper.save(update_fields=["in_pool"])
        people = [
            ("Demo author (empirical example)", "en", papers["empirical"], "author", True),
            ("示例作者（理论示例）", "zh-hans", papers["theory"], "author", True),
            # Invited to review the scored empirical example; may also choose the open demo paper.
            ("Demo invited expert (chooses a paper)", "en", papers["empirical"], "invited_expert", False),
        ]
        for name, lang, paper, relationship, current in people:
            contributor, _ = Contributor.objects.get_or_create(display_name=name, defaults={"preferred_language": lang})
            assignment, _ = Assignment.objects.get_or_create(contributor=contributor, paper=paper,
                                                             defaults={"relationship_to_paper": relationship})
            if current:
                contributor.current_assignment = assignment
                contributor.save(update_fields=["current_assignment"])
            if no_invitations:
                self.stdout.write(f"{contributor}")
                continue
            invitation, raw = issue_invitation(contributor, ACTOR)
            opens = paper.paper_id if current else "(chooses a paper)"
            self.stdout.write(f"{name} -> {opens}: {invitation.link(raw)}")
        self.stdout.write(self.style.SUCCESS("Demo loaded: fictional examples only. Links are shown only now."))
