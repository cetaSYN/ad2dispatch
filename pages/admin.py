from django.contrib import admin
from .models import Page


class PageAdmin(admin.ModelAdmin):
    fields = ['order', 'raw', 'title', 'content', 'edited_by', 'edited_date', 'parent_page']
    list_display = ['order', 'parent_page', 'title', 'content_preview', 'edited_date', 'edited_by']
    search_fields = ['title', 'content']
    ordering = ('parent_page', 'order',)


admin.site.register(Page, PageAdmin)
