from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from .models import Page
from .views import page


class PageTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(
            username='testuser', email='test@...', password='secret',
        )
        self.user.save()
        test_page = Page(
            title='test'
        )
        test_page.save()
        test_child = Page(
            parent_page=Page.objects.get(title='test'), title='child_test'
        )
        test_child.save()

    def test_page_output(self):
        # Page
        request = self.factory.get('/test/')
        request.user = AnonymousUser()

        response = page(request, 'test')
        self.assertEqual(response.status_code, 200)

        # Child Page
        request = self.factory.get('/test/child_test')
        request.user = AnonymousUser()

        response = page(request, 'test', 'child_test')
        self.assertEqual(response.status_code, 200)

        # Missing Page
        request = self.factory.get('/badtest/')
        request.user = AnonymousUser()

        try:
            page(request, 'badtest')
            self.fail('404 not thrown.')
        except Http404:
            pass

        # Missing Child Page
        request = self.factory.get('/test/badtest')
        request.user = AnonymousUser()

        try:
            page(request, 'test', 'badtest')
            self.fail('404 not thrown.')
        except Http404:
            pass
