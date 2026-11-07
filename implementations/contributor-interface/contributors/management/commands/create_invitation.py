import getpass

from django.core.management.base import BaseCommand, CommandError

from contributors.models import Assignment, Contributor, issue_invitation
from papers.models import log_event


class Command(BaseCommand):
    help = ("Create a contributor's personal link and print it once; earlier links are revoked. Only its hash is stored. "
            "Given an assignment (a-...), the link opens that paper; given a contributor (c-...), it opens their "
            "current paper, or the page for choosing one.")

    def add_arguments(self, parser):
        parser.add_argument("public_id", help="A contributor's public ID (c-...) or an assignment's (a-...).")
        parser.add_argument("--days", type=int, default=None, help="Days until the link expires (default: DEEPECON_INVITATION_DAYS).")

    def handle(self, public_id, days=None, **options):
        actor = f"cli:{getpass.getuser()}"
        assignment = Assignment.objects.select_related("contributor", "paper").filter(public_id=public_id).first()
        if assignment is not None:
            contributor = assignment.contributor
            contributor.current_assignment = assignment
            contributor.save(update_fields=["current_assignment"])
            log_event(actor, "current_paper_set", assignment, by="team")
        else:
            contributor = Contributor.objects.filter(public_id=public_id).first()
            if contributor is None:
                raise CommandError(f"No contributor or assignment {public_id}.")
        invitation, raw = issue_invitation(contributor, actor, days)
        current = contributor.current()
        opens = current.paper.paper_id if current else "the page for choosing a paper"
        self.stdout.write(f"{contributor.public_id} -> {opens}: {invitation.link(raw)}  "
                          f"(expires {invitation.expires_at:%Y-%m-%d}; shown only now)")
