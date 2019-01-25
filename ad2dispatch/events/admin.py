from django.contrib import admin
from .models import Event, EventVolunteer, VolunteerType


class EventAdmin(admin.ModelAdmin):
    fields = ['title', 'date_time', 'duration', 'list_date', 'location', 'attire', 'details']
    list_display = ['summary', 'duration']
    search_fields = ['title', 'date_time']
    ordering = ['date_time']


class EventVolunteerAdmin(admin.ModelAdmin):
    fields = ['volunteer', 'event', 'type']
    list_display = ['volunteer', 'event', 'type']
    ordering = ('event', 'type')


class VolunteerTypeAdmin(admin.ModelAdmin):
    fields = ['type', 'max_volunteers', 'instructions', 'hidden']
    list_display = ['type']
    ordering = ('type', 'max_volunteers', 'hidden', 'instructions')


admin.site.register(Event, EventAdmin)
admin.site.register(EventVolunteer, EventVolunteerAdmin)
admin.site.register(VolunteerType, VolunteerTypeAdmin)
