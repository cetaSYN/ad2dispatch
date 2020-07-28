from django.conf import settings


def org_info(request):
    return {
        'DISCLAIMER': settings.DISCLAIMER,
    }