from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Article(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                   related_name='created_by',
                                   limit_choices_to={'is_staff': True})
    created_date = models.DateTimeField(default=timezone.now)
    edited_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                  related_name='edited_by',
                                  limit_choices_to={'is_staff': True},
                                  null=True,
                                  blank=True)
    edited_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return self.title

    def was_edited(self):
        return self.created_date != self.edited_date
