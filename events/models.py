from django.db import models
from volunteers import models as vol_model
from installations import models as ins_model


class Event(models.Model):
    installation = models.ForeignKey(
        ins_model.Installation,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length=128)
    date_time = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=128)
    details = models.TextField(null=True, blank=True)
    display_on = models.DateField(null=True, blank=True)
    lock_in = models.DurationField()


class VolunteerType(models.Model):
    max_volunteers = models.IntegerField(max_length=5)
    instructions = models.TextField()
    required_installation_group = models.ForeignKey(
        ins_model.InstallationGroup,
        on_delete = models.CASCADE
    )


class EventVolunteer(models.Model):
    volunteer = models.ForeignKey(
        vol_model.Volunteer,
        on_delete = models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        on_delete = models.CASCADE
    )
    volunteer_type = models.ForeignKey(
        VolunteerType,
        on_delete = models.CASCADE
    )
    ready = models.BooleanField(
        default = False,
        help_text = 'True if volunteer has identified themselves as "ready" for the event'
    )
