from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Volunteer


class VolunteerInline(admin.StackedInline):
    model = Volunteer
    can_delete = False
    verbose_name_plural = 'volunteers'


class UserAdmin(UserAdmin):
    inlines = (VolunteerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
