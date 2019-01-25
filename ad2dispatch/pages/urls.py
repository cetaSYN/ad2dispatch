from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.page, name='page'),
    url(r'^(?P<page_title>[a-zA-Z0-9 _-]+)/$', views.page, name='page'),
    url(r'^(?P<page_title>[a-zA-Z0-9 _-]+)/(?P<sub_page>[a-zA-Z0-9 _-]+)/$',
        views.page, name='page'),
]
