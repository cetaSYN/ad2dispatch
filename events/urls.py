from django.conf.urls import url

from events import views

url_patterns = [
    url("<str:installation>/", views.index, name="events:index"),
    url("<str:installation>/details/", views.index_details, name="events:index_details"),
    url("<str:installation>/create/", views.event_create, name="events:event_create"),
    url("<int:event_id>/", views.event_details, name="events:event_details"),
    url("<int:event_id>/update/", views.update_event, name="events:update_event"),
    url("<int:event_id>/delete/", views.delete_event, name="events:delete_event"),
]
