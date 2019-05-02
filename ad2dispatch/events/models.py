from __future__ import print_function
from __future__ import unicode_literals

from datetime import timedelta

from django.template import defaultfilters
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class VolunteerType(models.Model):
    type = models.CharField(max_length=16, null=False, unique=False, help_text='Name of volunteer type')
    common = models.BooleanField(null=False, blank=False, default=False, help_text='Common type. If checked, will prevent the system from hiding the type after a week')
    default = models.BooleanField(null=False, blank=False, default=False, help_text='If checked, this type will be added to new events by default. Assumes Common')
    max_volunteers = models.IntegerField(null=True, blank=True, help_text='Maximum volunteers allowed for an event')
    instructions = models.TextField(null=False, help_text='Instructions given to volunteers of this type upon volunteering')
    hidden = models.BooleanField(null=False, blank=False, default=False, help_text='If checked, will only be shown to users with the view_hidden_events and vol_hidden_events permissions')
    created = models.DateField(null=False, blank=False, auto_now_add=True)  # Used exclusively for expiring uncommon volunteer types to prevent clutter

    class Meta:
        default_permissions = ()
        permissions = (("view_hidden_events", "Can view hidden events"),
                       ("vol_hidden_events", "Can volunteer for hidden events"))

    def __str__(self):
        return self.type


class EventVolunteer(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=False)
    # 'Event' defined below, referenced by name
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


def default_types():
    return VolunteerType.objects.filter(default=True)


def common_or_recent_types():
    return Q(common=True) | Q(default=True) | Q(created__gt=timezone.now() + timedelta(days=7))


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
    types = models.ManyToManyField(VolunteerType, default=default_types, limit_choices_to=common_or_recent_types)

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
        return (timezone.localtime(self.date_time) - timezone.now()).days

    def volunteers_type(self, voltype):
        return EventVolunteer.objects.filter(event=self, type=voltype)

    def num_volunteers_type(self, voltype):
        return EventVolunteer.objects.filter(event=self, type=voltype).count()

    def is_during_event(self):
        return timezone.now() > self.date_time and \
            timezone.now < (self.date_time + self.duration)


def do_unvolunteer(vol_event):
    sel = EventVolunteer.objects.get(volunteer=vol_event.volunteer,
                                     event=vol_event.event,
                                     type=vol_event.type)
    sel.delete()


def get_event_volunteer(user, event_id, type_name):
    return EventVolunteer(
        volunteer=user,
        event=Event.objects.get(pk=event_id),
        type=VolunteerType.objects.get(type=type_name))


def get_volunteers(events):
    volunteers = EventVolunteer.objects.filter(
        event__in=events
    ).order_by('type')
    if volunteers:
        for volunteer in volunteers:
            volunteer.profile = volunteer.get_profile()
    return volunteers


def position_is_full(event, type):
    max_vols = VolunteerType.objects.get(pk=type).max_volunteers
    if max_vols is None:
        return False
    return EventVolunteer.objects.filter(
        event=Event.objects.get(pk=event),
        type=VolunteerType.objects.get(pk=type)).count() >= max_vols
