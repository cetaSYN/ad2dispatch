from __future__ import print_function
from __future__ import unicode_literals

from datetime import timedelta

from django.template import defaultfilters
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=32, null=False)
    date_time = models.DateTimeField(null=False)
    duration = models.DurationField(null=False,  # Max of 9 days per bigint
                                    help_text='Format as hh:mm:ss')
    location = models.CharField(max_length=64, null=True, blank=True)
    attire = models.CharField(max_length=64, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    list_date = models.DateField(null=True, blank=True,
                                 help_text='Date that the event should be ' +
                                 'added to the availability listing. '
                                 'Leaving this blank will add it 30 days ' +
                                 'prior to the start.')

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.title + ' - ' + defaultfilters.date(
            timezone.localtime(self.date_time), "(D) d M: Hi")

    def summary(self):
        return self

    def end_date_time(self):
        return self.date_time + self.duration

    def days_until(self):
        return timezone.localtime(self.date_time).day - timezone.now().day

    def days_until_msg(self):
        if self.days_until() == 0:
            return 'Today!'
        else:
            return str(self.days_until()) + ' days away'

    def volunteers_type(self, voltype):
        return EventVolunteer.objects.filter(event=self, type=voltype)

    def num_volunteers_type(self, voltype):
        return EventVolunteer.objects.filter(event=self, type=voltype).count()

    def is_during_event(self):
        return timezone.now() > self.date_time and \
            timezone.now < (self.date_time + self.duration)


def position_is_full(event, type):
    max_vols = VolunteerType.objects.get(pk=type).max_volunteers
    if max_vols is None:
        return False
    return EventVolunteer.objects.filter(
        event=Event.objects.get(pk=event),
        type=VolunteerType.objects.get(pk=type)).count() >= max_vols


def get_running_events():
    return Event.objects.filter(date_time__lt=timezone.now(),
                                date_time__gt=(timezone.now() +
                                timedelta(days=-1)))  # TODO Not timedelta


class VolunteerType(models.Model):
    type = models.CharField(max_length=16, null=False)
    max_volunteers = models.IntegerField(null=True, blank=True)
    instructions = models.TextField(null=False)
    hidden = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        default_permissions = ()
        permissions = (("view_hidden_events", "Can view hidden events"),
                       ("vol_hidden_events", "Can volunteer for hidden events"))

    def __str__(self):
        return self.type


def get_volunteers(events):
    volunteers = EventVolunteer.objects.filter(
        event__in=events
    ).order_by('type')
    if volunteers:
        for volunteer in volunteers:
            volunteer.profile = volunteer.get_profile()
    return volunteers


class EventVolunteer(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False)
    type = models.ForeignKey(VolunteerType, on_delete=models.CASCADE,
                             null=False)

    class Meta:
        default_permissions = ()

    def has_volunteered(self):
        if EventVolunteer.objects.filter(volunteer=self.volunteer,
                                         event=self.event,
                                         type=self.type).count() > 0:
            return True
        return False

    def get_profile(self):
        from userprofiles.models import Volunteer
        return Volunteer.objects.get(user=self.volunteer)


def do_unvolunteer(vol_event):
    sel = EventVolunteer.objects.get(volunteer=vol_event.volunteer,
                                     event=vol_event.event,
                                     type=vol_event.type)
    sel.delete()


def has_upcoming_vol(user, type):
    if EventVolunteer.objects.filter(
            volunteer=user,
            type=VolunteerType.objects.get(type=type),
            event__in=Event.objects.filter(date_time__lt=timezone.now() +
                                           timedelta(days=30))).count() > 0:
        return True
