from django.db import models
from volunteers import models as vol_model
from installations import models as ins_model


class Event(models.Model):
    installation = models.ForeignKey(
        ins_model.Installation,
        on_delete=models.CASCADE,
        help_text="Reference to the installation at which the event is occurring",
    )
    title = models.CharField(max_length=128, help_text="Title of the event")
    date_time = models.DateTimeField(help_text="Datetime of the start of the event")
    duration = models.DurationField(help_text="Duration of the event")
    location = models.CharField(max_length=128, help_text="Location of the event")
    details = models.TextField(null=True, blank=True, help_text="Additional details of the event")
    display_on = models.DateField(
        null=True, blank=True, help_text="Date and time to begin displaying the event to volunteers"
    )
    lock_in = models.DurationField(help_text="Duration prior to the event during which volunteers may not cancel")


class VolunteerPosition(models.Model):
    max_volunteers = models.IntegerField(help_text="Maximum number of volunteers for the position")
    instructions = models.TextField(help_text="Instructions for the volunteers regarding their position")
    required_installation_group = models.ForeignKey(
        ins_model.InstallationGroup,
        on_delete=models.CASCADE,
        help_text="The installation group the volunteer must belong to to volunteer for the position",
    )


class EventVolunteer(models.Model):
    volunteer = models.ForeignKey(
        vol_model.Volunteer, on_delete=models.CASCADE, help_text="The Volunteer for the event"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text="The event being volunteered for")
    volunteer_position = models.ForeignKey(
        VolunteerPosition, on_delete=models.CASCADE, help_text="The position being volunteered for"
    )
    ready = models.BooleanField(
        default=False, help_text='True if volunteer has identified themselves as "ready" for the event'
    )
