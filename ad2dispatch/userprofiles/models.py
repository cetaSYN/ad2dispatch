import functools

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from events.models import EventVolunteer


class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=24, null=True,
                               blank=True,
                               default='USAF')
    rank = models.CharField(max_length=16, null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True)
    phone_number_2 = models.CharField(max_length=14, null=True, blank=True)
    vehicle_desc = models.CharField(max_length=128, null=True)
    ready = models.BooleanField(default=False, editable=True,
                                help_text='If driver has marked themselves ' +
                                'as \'ready\' for the event duration.')
    dispatched = models.BooleanField(default=False, editable=False)
    council_pos = models.CharField(max_length=24, null=True, blank=True)
    sup_name = models.CharField(max_length=64, null=True)
    sup_phone = models.CharField(max_length=14, null=True)
    location = models.DecimalField(max_digits=9, decimal_places=6,
                                   null=True,
                                   blank=True)
    accepted_waiver = models.BooleanField(default=False)

    @property
    def hours_total(self):
        hours = None
        try:
            hours = functools \
                .reduce(lambda x, y: x+y,
                        [e_vols.event.duration.seconds // 3600 for e_vols in
                         EventVolunteer.objects.filter(volunteer=self.user)
                         if e_vols.event.date_time <= timezone.now()])
        except TypeError as terr:
            pass  # Empty set
        return hours

    # @property
    # def hours_yearly(self):
    #     return [e_vols.event.duration for e_vols in
    #             EventVolunteer.objects.get(volunteer=self)
    #             if e_vols.date_time > #the start date of the current year]

    def is_populated(self):
        if all([self.user, self.phone_number, self.vehicle_desc,
                self.sup_name, self.sup_phone]):
            return True
        else:
            return False

    def is_ready(self):
        if self.ready and not self.dispatched:
            return True
        return False
