from django.db import models
from django.utils import timezone
from volunteers import models as vol_models
from events import models as ev_models


class Installation(models.Model):
    """An ad2 organization at an installation"""

    latitude = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        help_text="3 decimal places (~100m of GPS precision)",  # Includes decimal length
    )
    longitude = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        help_text="3 decimal places (~100m of GPS precision)",  # Includes decimal length
    )
    volunteer_policy = models.TextField(
        help_text="""Organizational policy that all drivers must agree to prior to volunteering.
                     May include standards on insurance, vehicle safety measures, liability, etc."""
    )

    def events(self):
        """Returns a collection of actively running events for this installation"""
        return ev_models.Event.objects.filter(
            installation=self, start_date_time__lt=timezone.now(), end_date_time__gt=timezone.now(),
        )


class InstallationVolunteer(models.Model):
    """A volunteer's information in relation to an installation organization"""

    volunteer = models.ForeignKey(vol_models.Volunteer, on_delete=models.CASCADE)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE)
    installation_verified = models.BooleanField(
        default=False,
        help_text="""True, if the installation organization has verified a volunteer.
                     Installation orgs cannot globally verify volunteers.""",
    )
    accepted_policies = models.BooleanField(
        default=False, help_text="True, if the volunteer has accepted the installation's volunteering policies",
    )


class InstallationGroup(models.Model):
    """A group belonging to an installation organization (e.g. Council Members)"""

    installation = models.ForeignKey(
        Installation, on_delete=models.CASCADE, help_text="Installation the group belongs to",
    )
    title = models.CharField(max_length=128, help_text="Title of the installation group")
    expiration_date = models.DateTimeField(help_text="The date and time when the user's access to the group expires")

    def is_expired(self):
        """True if the volunteer's access to the group has expired"""
        return timezone.now() < self.expiration_date


class InstallationPosition(models.Model):
    """A position belonging to an installation organization (e.g. Volunteer Coordinator)"""

    installation = models.ForeignKey(
        Installation, on_delete=models.CASCADE, help_text="Installation the position belongs to",
    )
    title = models.CharField(max_length=128, help_text="Title of the position")
    description = models.TextField(null=True, blank=True, help_text="Description of the duties of the position")
    expiration_date = models.DateTimeField(help_text="The date and time when the user's access to the position expires")

    def is_expired(self):
        """True if the volunteer's access to the position has expired"""
        return timezone.now() < self.expiration_date
