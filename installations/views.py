from django.http import HttpResponse
from django.views import View


class LocatorView(View):
    def get(self, request):
        return HttpResponse()
