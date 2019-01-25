from django.contrib import admin
# Register your models here.
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'created_by', 'created_date', 'edited_by', 'edited_date']
    list_display = ['title', 'created_date', 'created_by', 'edited_date', 'edited_by']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)
