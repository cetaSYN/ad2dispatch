from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Page(models.Model):
    parent_page = models.ForeignKey("Page", on_delete=models.SET_NULL,
                                    related_name='page_parent_page',
                                    null=True,
                                    blank=True)
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=64)
    content = models.TextField(null=True, blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                  related_name='page_edited_by',
                                  limit_choices_to={'is_staff': True},
                                  null=True,
                                  blank=True)
    edited_date = models.DateTimeField(null=True, blank=True)
    raw = models.BooleanField(null=False, default=False,
                              help_text='Toggles parsing of markdown ' +
                              '& display of styling')

    def __str__(self):
        return self.title

    def content_preview(self):
        return self.content[:64] + '...'

    def get_sub_pages(self):
        try:
            sub_pages = Page.objects.filter(
                parent_page=Page.objects.get(pk=self.id)).order_by('order')
            if len(sub_pages) is 0 and self.parent_page is not None:
                sub_pages = Page.objects.filter(
                    parent_page=Page.objects.get(
                        pk=self.parent_page.id)).order_by('order')
                for sub_page in sub_pages:
                    sub_page.loc = 'page:' + self.parent_page.title + ':' + \
                        sub_page.title
                    sub_page.path = '/' + self.parent_page.title + '/' + \
                        sub_page.title
            else:
                for sub_page in sub_pages:
                    sub_page.loc = 'page:' + self.title + '/' + sub_page.title
                    sub_page.path = '/' + self.title + '/' + sub_page.title
        except:
            sub_pages = None
        return sub_pages


def get_top_pages():
    top_pages = Page.objects.filter(parent_page=None).order_by('order')
    # Builds navigation list, and adds helpful attributes
    for tpage in top_pages:
        tpage.loc = 'page:' + tpage.title
        if tpage.title != 'Home':
            tpage.path = '/' + tpage.title
        else:
            tpage.path = '/'
    return top_pages
