from django.shortcuts import render
from django.views import View

from .models import Installation


class LocatorView(View):
    def get(self, request):
        context = {
            "installations": Installation.objects.all()
        }
        return render(request, "installation_select.html", context)


class InstallationView(View):
    def get(self, request, installation):
        context = {
            "installation": Installation.objects.get(slug=installation)
        }
        return render(request, "installation.html", context)
