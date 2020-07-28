from django.contrib import admin
from .models import NewsArticle, NewsArticleEdit

@admin.register(NewsArticle, NewsArticleEdit)
class NewsAdmin(admin.ModelAdmin):
    pass
