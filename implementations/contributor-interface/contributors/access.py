"""Session-based access for contributors (plan §2.3).

A contributor signs in only by opening an invitation link; there are no passwords and no
paper search. The session holds the invitation that was used, and every request checks it
again: once the team revokes the link, or it expires, the session ends. A session reaches
only that invitation's assignment. Every view checks the requested paper against it on the
server and answers 404 for any other paper, so guessed or copied URLs reveal nothing.
"""
from functools import wraps

from django.http import Http404
from django.shortcuts import render

from .models import Invitation

SESSION_KEY = "deepecon_invitation_id"


def current_invitation(request):
    """The session's invitation if it is still active; otherwise ends the session."""
    pk = request.session.get(SESSION_KEY)
    if not pk:
        return None
    invitation = (Invitation.objects.select_related("assignment__contributor", "assignment__paper")
                  .filter(pk=pk).first())
    if invitation is None or not invitation.is_active:
        request.session.flush()
        return None
    return invitation


def sign_in(request, invitation):
    request.session.cycle_key()           # a new session key on every invitation use
    request.session[SESSION_KEY] = invitation.pk


def contributor_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        invitation = current_invitation(request)
        if invitation is None:
            return render(request, "contributors/not_signed_in.html", status=403)
        request.invitation = invitation
        request.contributor = invitation.assignment.contributor
        return view(request, *args, **kwargs)
    return wrapper


def assignment_for(request, paper_id):
    assignment = request.invitation.assignment
    if assignment.paper.paper_id != paper_id:
        raise Http404("No such paper.")
    return assignment
