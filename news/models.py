from django.db import models
from django.utils import timezone
from installations import models as ins_model
from volunteers import models as vol_model


class NewsArticle(models.Model):
    installation = models.ForeignKey(
        ins_model.Installation, on_delete=models.CASCADE, help_text="Installation the news belongs to"
    )

    @property
    def title(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("-edited_date_time").first().title

    @property
    def content(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("-edited_date_time").first().content

    @property
    def edited_by(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("-edited_date_time").first().edited_by

    @property
    def edited_date_time(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("-edited_date_time").first().edited_date_time


class NewsArticleEdit(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, help_text="News article being edited")
    title = models.CharField(max_length=128, help_text="The new title of the news article")
    content = models.TextField(help_text="The new news article content")
    edited_by = models.ForeignKey(
        vol_model.Volunteer,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        help_text="Volunteer editing the news article",
    )
    edited_date_time = models.DateTimeField(
        default=timezone.now, help_text="Date and time that the news article was edited"
    )

    def original_article(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("edited_date_time").first()

    def current_article(self):
        return NewsArticleEdit.objects.filter(page=self.article).order_by("-edited_date_time").first()
