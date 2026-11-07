"""Session-based access for contributors (plan §2.3).

A contributor signs in only by opening an invitation link; there are no passwords and no
paper search. Every view checks the session's assignment against the requested paper on the
server, and answers 404 for papers the contributor is not assigned to, so guessed or copied
URLs reveal nothing.
"""
from functools import wraps

from django.http import Http404
from django.shortcuts import render

from .models import Assignment, Contributor

SESSION_KEY = "deepecon_contributor_id"


def current_contributor(request):
    pk = request.session.get(SESSION_KEY)
    return Contributor.objects.filter(pk=pk).first() if pk else None


def sign_in(request, contributor):
    request.session.cycle_key()           # a new session key on every invitation use
    request.session[SESSION_KEY] = contributor.pk


def contributor_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        contributor = current_contributor(request)
        if contributor is None:
            return render(request, "contributors/not_signed_in.html", status=403)
        request.contributor = contributor
        return view(request, *args, **kwargs)
    return wrapper


def assignment_for(request, paper_id):
    assignment = (Assignment.objects.select_related("paper", "contributor")
                  .filter(contributor=request.contributor, paper__paper_id=paper_id).first())
    if assignment is None:
        raise Http404("No such paper.")
    return assignment
