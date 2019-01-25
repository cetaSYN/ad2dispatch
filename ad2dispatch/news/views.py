import markdown
from django.http import Http404
from django.shortcuts import render

from pages.models import get_top_pages
from userprofiles.models import Volunteer
from .models import Article


def index(request):
    try:
        article_list = Article.objects.values(
            'id', 'title', 'created_date').order_by('-created_date')
        selected = Article.objects.latest('created_date')
    except Article.DoesNotExist:
        selected = Article(
            created_by=None,
            created_date=None,
            title='Placeholder',
            content='You are seeing this page because you do not ' +
            'have any other pages created.<br> Please add content in ' +
            'the <a href="/admin/">admin panel</a>.')

    # Parse Markdown
    try:
        selected.content = markdown.markdown(selected.content)
    except AttributeError:
        pass

    if hasattr(selected, 'created_by'):
        creator = Volunteer.objects.get(user=selected.created_by)
    else:
        creator = None

    top_pages = get_top_pages()

    context = {
        'top_pages': top_pages,
        'article_list': article_list,
        'selected': selected,
        'creator': creator,
        'loc': 'news:index',
    }
    return render(request, 'news/article.html', context)


def article(request, article_id):
    try:
        article_list = Article.objects.values('id', 'title', 'created_date').order_by('-created_date')
        selected = Article.objects.get(id=article_id)

        # Parse Markdown
        try:
            selected.content = markdown.markdown(selected.content)
        except AttributeError:
            pass

        top_pages = get_top_pages()

    except Article.DoesNotExist:
        raise Http404("Article does not exist.")
    context = {
        'top_pages': top_pages,
        'article_list': article_list,
        'selected': selected,
        'creator': Volunteer.objects.get(user=selected.created_by),
        'loc': 'news:article:' + str(article_id),
    }
    return render(request, 'news/article.html', context)
