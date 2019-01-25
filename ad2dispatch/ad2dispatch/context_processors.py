from django.conf import settings  # import the settings file


def org_info(request):
    return {
        'DEBUG': settings.DEBUG,
        'ORG_NAME': settings.ORG_NAME,
        'ORG_ACRONYM': settings.ORG_ACRONYM,
        'ORG_PHONE': settings.ORG_PHONE,
        'ORG_PHONE_DISPLAY': settings.ORG_PHONE_DISPLAY,
        'ORG_PHONE_ALT': settings.ORG_PHONE_ALT,
        'ORG_PHONE_ALT_DISPLAY': settings.ORG_PHONE_ALT_DISPLAY,
        'DISCLAIMER': settings.DISCLAIMER,
        'FACEBOOK': settings.FACEBOOK,
        'TWITTER': settings.TWITTER,
        'MAPS_KEY': settings.MAPS_KEY
    }
