from django.conf import settings
from django.db import models
from django.utils import timezone

SERVICES = [
    ("USAF", "Air Force"),
    ("ARMY", "Army"),
    ("NAVY", "Navy"),
    ("USMC", "Marine Corps"),
    ("USCG", "Coast Guard"),
    ("SPSE", "Military Spouse"),
    ("GCIV", "Government Civilian"),
    ("NONE", "Other/Not Applicable"),
]

# TODO: Rank-Service Matching w/ Title
RANKS = list()
RANKS.extend(["E-{}".format(r) for r in range(1, 10)])
RANKS.extend(["W-{}".format(r) for r in range(1, 6)])
RANKS.extend(["O-{}".format(r) for r in range(1, 11)])
# Convert to tuple-list
RANKS = [(r.replace("-", ""), r) for r in RANKS]
RANKS.append(("NONE", "Other/Not Applicable"))


class Volunteer(models.Model):
    """User-wrapper; adds volunteer-relevant fields"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="User associated with the volunteer"
    )
    email_verified = models.BooleanField(
        default=False, help_text="True if the volunteer's email address has been verified"
    )
    email_key = models.CharField(max_length=40, help_text="Key for verifying a volunteer's email address")
    key_expires = models.DateTimeField(help_text="The expiration date of the email verification key")
    latitude = models.DecimalField(
        max_digits=5,  # Includes decimal field
        decimal_places=2,
        help_text="2 decimal places (~1km of GPS precision for privacy)",
    )
    longitude = models.DecimalField(
        max_digits=5,  # Includes decimal field
        decimal_places=2,
        help_text="2 decimal places (~1km of GPS precision for privacy)",
    )
    globally_verified = models.BooleanField(
        default=False,
        help_text="""True, if the volunteer has had their identity verified by ad2dispatch.
                     Is not affected by installation-level verification.""",
    )
    service = models.CharField(choices=SERVICES, max_length=4, help_text="The military service of the volunteer")
    unit = models.CharField(max_length=128, help_text="The unit of the volunteer")
    rank = models.CharField(choices=RANKS, max_length=4, help_text="The rank of the volunteer")
    phone_number = models.CharField(max_length=24, help_text="The phone number of the volunteer")
    phone_number_alt = models.CharField(max_length=24, help_text="The alternate phone number of the volunteer")
    vehicle_description = models.CharField(max_length=256, help_text="The description of the volunteer's vehicle")
    supervisor_name = models.CharField(max_length=128, help_text="The name of the volunteer's supervisor")
    supervisor_phone_number = models.CharField(
        max_length=24, help_text="The phone number of the volunteer's supervisor"
    )
    dispatched = models.BooleanField(default=False, help_text="True if the volunteer is currently dispatched")
    profile_reviewed = models.DateField(
        default=timezone.now, help_text="True if the volunteer has reviewed their profile since the last change"
    )
