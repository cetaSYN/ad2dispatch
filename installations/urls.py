from django.urls import path

from .views import LocatorView, InstallationView

urlpatterns = [
    path("", LocatorView.as_view()),
    path("<slug:installation>/", InstallationView.as_view(), name="installation_page")
]
