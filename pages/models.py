from django.db import models
from django.utils import timezone
from installations import models as ins_model
from volunteers import models as vol_model


class Page(models.Model):
    installation = models.ForeignKey(
        ins_model.Installation, on_delete=models.CASCADE, help_text="Installation the page belongs to"
    )
    parent_page = models.ForeignKey("Page", on_delete=models.PROTECT, help_text="Parent page of this page")

    @property
    def title(self):
        return PageEdit.objects.filter(page=self.page).order_by("-edited_date_time").first().title

    @property
    def content(self):
        return PageEdit.objects.filter(page=self.page).order_by("-edited_date_time").first().content

    @property
    def edited_by(self):
        return PageEdit.objects.filter(page=self.page).order_by("-edited_date_time").first().edited_by

    @property
    def edited_date_time(self):
        return PageEdit.objects.filter(page=self.page).order_by("-edited_date_time").first().edited_date_time


class PageEdit(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, help_text="Page being edited")
    title = models.CharField(max_length=128, help_text="The new title of the page")
    content = models.TextField(help_text="The new page content")
    edited_by = models.ForeignKey(
        vol_model.Volunteer, on_delete=models.SET_NULL, null=True, blank=False, help_text="Volunteer editing the page"
    )
    edited_date_time = models.DateTimeField(default=timezone.now, help_text="Date and time that the page was edited")

    def original_page(self):
        return PageEdit.objects.filter(page=self.page).order_by("edited_date_time").first()

    def current_page(self):
        return PageEdit.objects.filter(page=self.page).order_by("-edited_date_time").first()
