from django.contrib import admin
from .models import Installation, InstallationVolunteer, InstallationGroup, InstallationGroupMember, InstallationPosition, InstallationPositionMember

@admin.register(Installation, InstallationVolunteer, InstallationGroup, InstallationGroupMember, InstallationPosition, InstallationPositionMember)
class InstallationAdmin(admin.ModelAdmin):
    pass
