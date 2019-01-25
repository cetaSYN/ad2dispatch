from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from userprofiles.models import Volunteer
from .models import Article
from .views import article, index


class ArticleTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(
            username='testuser', email='test@...', password='secret',
        )
        self.user.save()
        self.volunteer = Volunteer(user=self.user)
        self.volunteer.save()
        test_article = Article(
            created_by=User.objects.get(username='testuser'), title='title', content='content',
        )
        test_article.save()

    def test_article_output(self):
        # Index
        request = self.factory.get('/news/')
        request.user = AnonymousUser()

        response = index(request)
        self.assertEqual(response.status_code, 200)

        # Article (1 is populated)
        request = self.factory.get('/news/1/')
        request.user = AnonymousUser()

        response = article(request, 1)
        self.assertEqual(response.status_code, 200)

        # Missing (5 is unpopulated)
        request = self.factory.get('/news/5/')
        request.user = AnonymousUser()

        try:
            article(request, 5)
            self.fail('404 not thrown.')
        except Http404:
            pass
