import getpass

from django.core.management.base import BaseCommand, CommandError

from contributors.models import Assignment, Invitation
from papers.models import log_event


class Command(BaseCommand):
    help = "Create an invitation link for an assignment and print it once. Only its hash is stored."

    def add_arguments(self, parser):
        parser.add_argument("assignment_id", help="The assignment's public ID (a-...).")
        parser.add_argument("--days", type=int, default=None, help="Days until the link expires (default: DEEPECON_INVITATION_DAYS).")

    def handle(self, assignment_id, days=None, **options):
        assignment = Assignment.objects.filter(public_id=assignment_id).first()
        if assignment is None:
            raise CommandError(f"No assignment {assignment_id}.")
        invitation, raw = Invitation.issue(assignment, days)
        log_event(f"cli:{getpass.getuser()}", "invitation_issued", assignment, invitation_id=invitation.pk,
                  expires_at=invitation.expires_at.isoformat())
        self.stdout.write(f"{assignment}: {invitation.link(raw)}  (expires {invitation.expires_at:%Y-%m-%d}; shown only now)")
