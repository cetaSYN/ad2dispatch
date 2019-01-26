from __future__ import print_function

import json
import urllib
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings

from pages.models import get_top_pages
from .models import Event, EventVolunteer, VolunteerType, do_unvolunteer, \
    has_upcoming_vol, get_volunteers, get_running_events, position_is_full
from .forms import EventManageDateSelectForm


def upcoming_list(request):
    upcoming_events = \
        Event.objects.filter(
            Q(date_time__lt=timezone.now() + timedelta(days=30),
                date_time__gt=timezone.now()) |
            Q(list_date__lte=timezone.now()),
                date_time__gt=timezone.now()).order_by('date_time')

    top_pages = get_top_pages()
    context = {
        'events': upcoming_events,
        'top_pages': top_pages,
    }

    if request.method == 'POST':
        # Verify user is logged in if volunteering
        if not request.user.is_authenticated:
            return redirect('/accounts/login/?next=%s' % request.path)

        from userprofiles.models import Volunteer
        try:
            if not Volunteer.objects.get(user=request.user).is_populated():
                context['flash_type'] = 'warning'
                context['flash_message'] = \
                    '''You must first populate your
                    <a href="/accounts/profile/">profile</a>.'''
            elif not Volunteer.objects.get(user=request.user).accepted_waiver:
                context['flash_type'] = 'warning'
                context['flash_message'] = \
                    '''Before volunteering you must accept the waiver in your
                    <a href="/accounts/profile/">profile</a>.'''
            else:
                # Parse and verify type
                data = json.loads(
                    urllib.parse.unquote(
                        request.body.decode()
                        .split('&')[1]
                        .split('=')[0]
                    )
                )
                submitted_event = data['event']
                if not isinstance(submitted_event, int):
                    raise TypeError
                submitted_type = data['type']
                if not isinstance(submitted_type, int):
                    raise TypeError

                # Verify selected option is one that was presented
                presented = False
                for upcoming_event in upcoming_events:
                    if upcoming_event.pk == submitted_event:
                        presented = True
                        break
                if not presented:
                    raise Exception('Option unavailable')

                # Handle volunteer/unvolunteer
                vol_event = EventVolunteer(
                    volunteer=request.user,
                    event=Event.objects.get(pk=submitted_event),
                    type=VolunteerType.objects.get(pk=submitted_type))

                if not vol_event.has_volunteered():
                    if position_is_full(submitted_event, submitted_type):
                        context['flash_type'] = 'warning'
                        context['flash_message'] = \
                            'This position is already filled.'
                    else:
                        if vol_event.event.date_time.date() + timedelta(days=-1) == timezone.localdate():
                            context['flash_type'] = 'warning'
                            context['flash_message'] = \
                                '''If you volunteer on the same day as a shift,
                                 please call or text the on-call phone:
                                 <a href="{}">
                                 {}</a>.'''.format(
                                     settings.ORG_PHONE_ALT,
                                     settings.ORG_PHONE_ALT_DISPLAY
                                 )
                        vol_event.save()
                else:
                    do_unvolunteer(vol_event)
        except Volunteer.DoesNotExist:
            context['flash_type'] = 'warning'
            context['flash_message'] = \
                '''You must first populate your
                <a href="/accounts/profile/">profile</a>.'''

    for event in upcoming_events:
        if request.user.has_perm('events.view_hidden_events_volunteertype'):
            event.type = VolunteerType.objects.all()
        else:
            event.type = VolunteerType.objects.filter(hidden=False)
        for voltype in event.type:
            voltype.volnum = Event.num_volunteers_type(event, voltype=voltype)
            if request.user.is_authenticated:
                if EventVolunteer.objects.filter(
                        volunteer=request.user,
                        event=event,
                        type=voltype).count() > 0:
                    voltype.me = True

    if request.user.is_authenticated:
        volunteer = {
            'is_driver': has_upcoming_vol(
                user=request.user, type='driver'),
            'is_dispatcher': has_upcoming_vol(
                user=request.user, type='dispatcher'),
        }

        context['volunteer'] = volunteer

    return render(request, 'upcoming_list.html', context)


@login_required
def driver(request):
    instructions = VolunteerType.objects.get(type='Driver').instructions

    top_pages = get_top_pages()
    volunteer = {
        'is_driver': has_upcoming_vol(
            user=request.user, type='driver'),
        'is_dispatcher': has_upcoming_vol(
            user=request.user, type='dispatcher'),
    }

    context = {
        'instructions': instructions,
        'top_pages': top_pages,
        'volunteer': volunteer,
    }
    return render(request, 'driver.html', context)


@login_required
def dispatcher(request):
    instructions = VolunteerType.objects.get(type='Dispatcher').instructions

    top_pages = get_top_pages()
    volunteer = {
        'is_driver': has_upcoming_vol(
            user=request.user, type='driver'),
        'is_dispatcher': has_upcoming_vol(
            user=request.user, type='dispatcher'),
    }

    volunteers = get_volunteers(get_running_events())
    context = {
        'instructions': instructions,
        'volunteers': volunteers,
        'top_pages': top_pages,
        'volunteer': volunteer,
    }
    return render(request, 'dispatcher.html', context)


@login_required
def manage(request, start_date=None, end_date=None):
    context = {}
    if not request.user.has_perm('events.change_eventvolunteer'):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    try:
        start_date = datetime.strptime(start_date, "%d%b%y")
        end_date = datetime.strptime(end_date, "%d%b%y")
    except (ValueError, TypeError) as vtex:
        start_date = None
        end_date = None
        print("Invalid date recieved:\n{}".format(vtex))

    if start_date is None or end_date is None:
        start_date = timezone.now() - timedelta(days=30)
        end_date = timezone.now()

    if request.method == 'POST':
        filter_form = EventManageDateSelectForm(request.POST)
        if filter_form.is_valid():
            try:
                start_date = datetime.strptime(
                    filter_form.cleaned_data['start_date'], "%d%b%y")
                end_date = datetime.strptime(
                    filter_form.cleaned_data['end_date'], "%d%b%y")
            except (ValueError, TypeError) as vtex:
                print("Invalid date recieved:\n{}".format(vtex))
            return redirect(
                "/volunteer/manage/{}/{}".format(
                    start_date.strftime("%d%b%y"),
                    end_date.strftime("%d%b%y"))
                )
        else:
            context['flash_type'] = 'warning'
            context['flash_message'] = 'Could not parse dates'
    else:
        filter_form = EventManageDateSelectForm(initial={
            'start_date': start_date.strftime("%d%b%y"),
            'end_date': end_date.strftime("%d%b%y")
        })

    upcoming_events = Event.objects.filter(
            Q(date_time__lt=end_date + timedelta(days=1),
              date_time__gt=start_date)
        ).order_by('date_time')[:50]
    # This is stupid-inefficient
    for event in upcoming_events:
        event.type = VolunteerType.objects.all()
        for voltype in event.type:
            voltype.vol = EventVolunteer.objects.filter(
                event=event, type=voltype)
            # RIP performance
            for vol in voltype.vol:
                vol.profile = vol.get_profile()
            voltype.volnum = Event.num_volunteers_type(event, voltype=voltype)
            # if request.user.is_authenticated:
            #     if EventVolunteer.objects.filter(
            #             volunteer=request.user,
            #             event=event,
            #             type=voltype).count() > 0:
            #         voltype.me = True

    top_pages = get_top_pages()
    context['events'] = upcoming_events
    context['top_pages'] = top_pages
    context['form'] = filter_form

    return render(request, 'manage.html', context)


@login_required
def event(request, event_id):
    if not request.user.has_perm('events.change_eventvolunteer'):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    try:
        selected = Event.objects.filter(id=event_id)
        volunteers = get_volunteers(selected)

    except Event.DoesNotExist:
        from django.http import Http404
        raise Http404("Event does not exist.")
    top_pages = get_top_pages()
    context = {
        'top_pages': top_pages,
        'selected': selected,
        'volunteers': volunteers,
    }
    return render(request, 'event.html', context)
