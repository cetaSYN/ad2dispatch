from django.db import models
from volunteers import models as vol_model


class Installation(models.Model):
    latitude = models.DecimalField(
        max_digits = 6,  # Includes decimal length
        decimal_places = 3,
        help_text = '3 decimal places (~100m of GPS precision)'
    )
    longitude = models.DecimalField(
        max_digits = 6,  # Includes decimal length
        decimal_places = 3,
        help_text = '3 decimal places (~100m of GPS precision)'
    )
    volunteer_policy = models.TextField(
        help_text = '''Organizational policy that all drivers must agree to prior to volunteering.
                     May include standards on insurance, vehicle safety measures, liability, etc.'''
    )


class InstallationVolunteer(models.Model):
    volunteer = models.ForeignKey(
        vol_model.Volunteer,
        on_delete = models.CASCADE
    )
    installation = models.ForeignKey(
        Installation,
        on_delete = models.CASCADE
    )
    installation_verified = models.BooleanField(
        default = False,
        help_text = '''True, if the installation organization has verified a volunteer.
                     Installation orgs cannot globally verify volunteers.'''
    )
    accepted_policies = models.BooleanField(
        default = False,
        help_text='True, if the volunteer has accepted the installation\'s volunteering policies'
    )


class InstallationGroup(models.Model):
    installation = models.ForeignKey(
        Installation,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length=128)


class InstallationPosition(models.Model):
    installation = models.ForeignKey(
        Installation,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
