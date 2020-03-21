from django.urls import path

from .views import LocatorView

urlpatterns = [
    path('', LocatorView.as_view())
]