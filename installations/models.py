from django.db import models
from django.utils import timezone
from volunteers import models as vol_models
from events import models as ev_models


class Installation(models.Model):
    """An ad2 organization at an installation"""

    title = models.CharField(max_length=128, help_text="Title of the installation organization")
    slug = models.SlugField(help_text="The url slug of the installation. NOTE: Editing this field may break links")
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
        """Returns a collection of actively running events for this installation sorted by start time"""
        return ev_models.Event.objects.filter(
            installation=self, start_date_time__lt=timezone.now(), end_date_time__gt=timezone.now(),
        ).order_by("-start_date_time")


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
    can_mod_config = models.BooleanField(
        help_text="True if the group can modify the installation organization configuration"
    )
    can_mod_pages = models.BooleanField(help_text="True if the group can modify the installation organization's pages")
    can_mod_news = models.BooleanField(
        help_text="True if the group can modify the installation organization's news articles"
    )
    can_mod_volunteers = models.BooleanField(
        help_text="True if the group can modify the installation organization volunteers' statuses"
    )
    can_verify_volunteers = models.BooleanField(
        help_text="True if the group can verify volunteers at the installation organization level"
    )


class InstallationGroupMember(models.Model):
    """A volunteer belonging to an installation group"""

    volunteer = models.ForeignKey(
        InstallationVolunteer, on_delete=models.CASCADE, help_text="The volunteer in the installation group"
    )
    installation_group = models.ForeignKey(
        InstallationGroup, on_delete=models.CASCADE, help_text="The installation group the volunteer is in"
    )
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
    can_mod_config = models.BooleanField(
        help_text="True if the position can modify the installation organization configuration"
    )
    can_mod_pages = models.BooleanField(
        help_text="True if the position can modify the installation organization's pages"
    )
    can_mod_news = models.BooleanField(
        help_text="True if the position can modify the installation organization's news articles"
    )
    can_mod_volunteers = models.BooleanField(
        help_text="True if the position can modify the installation organization volunteers' statuses"
    )
    can_verify_volunteers = models.BooleanField(
        help_text="True if the position can verify volunteers at the installation organization level"
    )


class InstallationPositionMember(models.Model):
    """A volunteer belonging to an installation group"""

    volunteer = models.ForeignKey(
        InstallationVolunteer, on_delete=models.CASCADE, help_text="The volunteer is the installation position"
    )
    installation_position = models.ForeignKey(
        InstallationPosition, on_delete=models.CASCADE, help_text="The installation position the volunteer holds"
    )
    expiration_date = models.DateTimeField(help_text="The date and time when the user's access to the group expires")

    def is_expired(self):
        """True if the volunteer's access to the group has expired"""
        return timezone.now() < self.expiration_date
