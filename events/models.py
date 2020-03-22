from django.db import models
from django.utils import timezone
from volunteers import models as vol_model
from installations import models as ins_model


class Event(models.Model):
    """An event that can be volunteered for"""

    installation = models.ForeignKey(
        ins_model.Installation,
        on_delete=models.CASCADE,
        help_text="Reference to the installation at which the event is occurring",
    )
    title = models.CharField(max_length=128, help_text="Title of the event")
    start_date_time = models.DateTimeField(help_text="Date and time of the start of the event")
    duration = models.DurationField(help_text="Duration of the event")
    location = models.CharField(max_length=128, help_text="Location of the event")
    details = models.TextField(null=True, blank=True, help_text="Additional details of the event")
    display_on_date_time = models.DateField(
        null=True, blank=True, help_text="Date and time to begin displaying the event to volunteers",
    )
    lock_in = models.DurationField(help_text="Duration prior to the event during which volunteers may not cancel")

    @property
    def end_date_time(self):
        """Date and time of the end of the event"""
        return self.start_date_time + self.duration

    def is_occurring(self):
        """True if the event is in progress"""
        return self.end_date_time < self.start_date_time < timezone.now()

    def days_utils(self):
        """Returns the number of days until the start of the event"""
        return (timezone.localtime(self.start_date_time) - timezone.now()).days

    def volunteers_of_position(self, event_position):
        """Returns the volunteers for the current event of a given position"""
        return EventVolunteer.objects.filter(event=self, event_position=event_position)


class EventPosition(models.Model):
    """A position that can be volunteered for at an event (e.g. Driver)"""

    max_volunteers = models.IntegerField(help_text="Maximum number of volunteers for the position")
    instructions = models.TextField(help_text="Instructions for the volunteers regarding their position")
    required_installation_group = models.ForeignKey(
        ins_model.InstallationGroup,
        on_delete=models.CASCADE,
        help_text="The installation group the volunteer must belong to to volunteer for the position",
    )

    def is_full(self, event):
        """True if the position has reached volunteer capacity"""
        return EventVolunteer.objects.filter(event=event, event_position=self).count() >= self.max_volunteers


class EventVolunteer(models.Model):
    """A volunteer in relation to an event and position"""

    volunteer = models.ForeignKey(
        vol_model.Volunteer, on_delete=models.CASCADE, help_text="The Volunteer for the event",
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text="The event being volunteered for")
    event_position = models.ForeignKey(
        EventPosition, on_delete=models.CASCADE, help_text="The position being volunteered for",
    )
    ready = models.BooleanField(
        default=False, help_text='True if volunteer has identified themselves as "ready" for the event',
    )

    def unvolunteer(self):
        """Removes the volunteer from the event position"""
        self.delete()
