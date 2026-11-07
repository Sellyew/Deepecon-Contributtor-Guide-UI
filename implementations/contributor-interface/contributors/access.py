"""Session-based access for contributors (plan §2.3; D-044).

A contributor signs in only by opening their personal link; there are no passwords and no
search. The session holds the link that was used and checks it on every request: revoking
the link ends the session. Its expiry only stops new sign-ins, so a session already opened
lasts until the link is revoked, or until it has not been used for SESSION_COOKIE_AGE (a
year; every request renews it) (D-044, P-060).

The link opens one paper at a time, the contributor's current paper. Every view checks the
requested paper against it on the server. Another paper offered to the contributor leads to
the page that asks whether to switch to it; any other paper answers 404, so guessed or
copied URLs reveal nothing.
"""
from functools import wraps

from django.http import Http404
from django.shortcuts import redirect, render

from .models import Invitation

SESSION_KEY = "deepecon_invitation_id"


class NotCurrentPaper(Exception):
    """The paper is offered to the contributor but is not the one their link opens now."""

    def __init__(self, paper_id):
        super().__init__(paper_id)
        self.paper_id = paper_id


def current_invitation(request):
    """The session's link unless it has been revoked; otherwise ends the session."""
    pk = request.session.get(SESSION_KEY)
    if not pk:
        return None
    invitation = (Invitation.objects.select_related("contributor__current_assignment__paper")
                  .filter(pk=pk).first())
    if invitation is None or invitation.revoked_at is not None:
        request.session.flush()
        return None
    return invitation


def sign_in(request, invitation):
    request.session.cycle_key()           # a new session key on every use of the link
    request.session[SESSION_KEY] = invitation.pk


def contributor_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        invitation = current_invitation(request)
        if invitation is None:
            return render(request, "contributors/not_signed_in.html", status=403)
        request.invitation = invitation
        request.contributor = invitation.contributor
        try:
            return view(request, *args, **kwargs)
        except NotCurrentPaper as other:
            return redirect("contributors:choose", paper_id=other.paper_id)
    return wrapper


def assignment_for(request, paper_id):
    """The current assignment if it is for `paper_id`."""
    current = request.contributor.current()
    if current is not None and current.paper.paper_id == paper_id:
        return current
    if request.contributor.choosable_papers().filter(paper_id=paper_id).exists():
        raise NotCurrentPaper(paper_id)
    raise Http404("No such paper.")
