import markdown
from django.http import Http404
from django.shortcuts import render

from .models import Page, get_top_pages


def page(request, page_title=None, sub_page=None):
    try:
        # Get page data
        if page_title is None:
            selected_page = Page.objects.filter(
                parent_page=None).order_by('order').first()
            if selected_page is None:
                selected_page = Page(
                    parent_page=None,
                    order=0,
                    title='Welcome!',
                    content='This is the homepage. Please add your own '+
                            'in the <a href="/admin/">admin panel</a>.',
                    edited_by=None,
                    edited_date=None,
                    raw=False)
            selected_page.loc = 'page:' + selected_page.title
        elif sub_page is not None:
            selected_page = Page.objects.get(title=sub_page)
            selected_page.loc = 'page:' + page_title + ':' + selected_page.title
        else:
            selected_page = Page.objects.get(title=page_title)
            selected_page.loc = 'page:' + selected_page.title

        # Parse Markdown if not Raw
        if not selected_page.raw:
            try:
                selected_page.content = markdown.markdown(
                    selected_page.content)
            except AttributeError:
                pass

        top_pages = get_top_pages()
        sub_pages = selected_page.get_sub_pages()

    except Page.DoesNotExist:
        raise Http404("Page does not exist.")
    context = {
        'page': selected_page,
        'top_pages': top_pages,
        'sub_pages': sub_pages,
        'loc': selected_page.loc,
    }
    return render(request, 'pages/page.html', context)
