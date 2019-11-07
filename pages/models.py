from django.db import models
from django.utils import timezone
from installations import models as ins_model
from volunteers import models as vol_model


class Page(models.Model):
    installation = models.ForeignKey(
        ins_model.Installation,
        on_delete = models.CASCADE
    )
    parent_page = models.ForeignKey(
        'Page',
        on_delete = models.PROTECT
    )
    created_by = models.ForeignKey(
        vol_model.Volunteer,
        on_delete = models.SET_NULL,
        null = True,
        blank = False
    )
    created_date_time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=128)
    content = models.TextField()


class PageEdit(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete = models.CASCADE
    )
    edited_by = models.ForeignKey(
        vol_model.Volunteer,
        on_delete = models.SET_NULL,
        null = True,
        blank = False
    )
    edited_date_time = models.DateTimeField(default=timezone.now)
    new_title = models.CharField(max_length=128)
    content_diff = models.TextField()
