import getpass

from django.core.management.base import BaseCommand, CommandError

from contributors.models import Assignment, Contributor, issue_invitation, set_first_paper


class Command(BaseCommand):
    help = ("Create a contributor's personal link and print it once; earlier links are revoked. Only its hash is stored. "
            "The link opens the contributor's current paper, or the page for choosing one. Given an assignment (a-...), "
            "that paper becomes the current paper if the contributor has none; a paper they chose is kept (D-044).")

    def add_arguments(self, parser):
        parser.add_argument("public_id", help="A contributor's public ID (c-...) or an assignment's (a-...).")
        parser.add_argument("--days", type=int, default=None, help="Days until the link expires (default: DEEPECON_INVITATION_DAYS).")

    def handle(self, public_id, days=None, **options):
        actor = f"cli:{getpass.getuser()}"
        assignment = Assignment.objects.select_related("contributor", "paper").filter(public_id=public_id).first()
        note = ""
        if assignment is not None:
            contributor = assignment.contributor
            note = set_first_paper(contributor, assignment, actor)
        else:
            contributor = Contributor.objects.filter(public_id=public_id).first()
            if contributor is None:
                raise CommandError(f"No contributor or assignment {public_id}.")
        invitation, raw = issue_invitation(contributor, actor, days)
        current = contributor.current()
        if current is not None:
            opens = current.paper.paper_id
        elif contributor.choosable_papers().exists():
            opens = "the page for choosing a paper"
        else:
            opens = "the page for choosing a paper, which is empty: assign or open a paper first"
        self.stdout.write(f"{contributor.public_id} -> {opens}: {invitation.link(raw)}  "
                          f"(expires {invitation.expires_at:%Y-%m-%d}; shown only now)")
        if note:
            self.stdout.write(self.style.WARNING(f"Note: {note}."))
