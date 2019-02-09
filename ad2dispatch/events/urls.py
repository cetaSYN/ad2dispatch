from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.upcoming_list, name='upcoming_list'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^manage/' +
        r'(?P<start_date>[0-9]{2}[A-Za-z]{3}[0-9]{2})/' +
        r'(?P<end_date>[0-9]{2}[A-Za-z]{3}[0-9]{2})/$',
        views.manage, name='manage'),
    url(r'^event/(?P<event_id>[0-9]+)/manage/$', views.event_manage, name='event_manage'),
    url(r'^event/(?P<event_id>[0-9]+)/(?P<type_name>[A-Za-z_0-9\-]+)/$', views.event, name='event'),
]
