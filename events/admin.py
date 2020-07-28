from django.contrib import admin
from .models import Event, EventPosition, EventVolunteer

@admin.register(Event, EventPosition, EventVolunteer)
class EventAdmin(admin.ModelAdmin):
    pass
