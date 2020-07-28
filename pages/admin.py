from django.contrib import admin
from .models import Page, PageEdit

@admin.register(Page, PageEdit)
class PageAdmin(admin.ModelAdmin):
    pass
