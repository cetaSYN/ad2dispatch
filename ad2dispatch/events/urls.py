from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.upcoming_list, name='upcoming_list'),
    url(r'^driver/$', views.driver, name='driver'),  # TODO Don't hardcode
    url(r'^dispatcher/$', views.dispatcher, name='dispatcher'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^manage/' +
        r'(?P<start_date>[0-9]{2}[A-Za-z]{3}[0-9]{2})/' +
        r'(?P<end_date>[0-9]{2}[A-Za-z]{3}[0-9]{2})/$',
        views.manage, name='manage'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event')
]
