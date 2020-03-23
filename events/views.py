from django.http import Http404
from django.shortcuts import render

from installations import models as ins_models

# from events import models as ev_models


def index(request, installation):
    """Listing of publicly available volunteer opportunities for the given installation"""
    try:
        return render(
            request, "index.html", {"events": ins_models.Installation.objects.get(slug=installation).events()},
        )
    except ins_models.Installation.DoesNotExist:
        raise Http404


def index_details(request, installation):
    """Listing of volunteer oppotunities for the installation with current volunteer info"""
    # TODO: Not yet implemented
    context = dict()
    try:
        # events = ins_models.Installation.objects.get(slug=installation).events()
        return render(request, "index_details.html", context)
    except ins_models.Installation.DoesNotExist:
        raise Http404


def event_create(request, installation):
    # if ins_models
    pass


def event_details(request, event_id):
    pass


def event_update(request, event_id):
    pass


def event_delete(request, event_id):
    pass
