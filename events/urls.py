from django.urls import path

from events import views

urlpatterns = [
    path("<str:installation>/", views.index),
    path("<str:installation>/details/", views.index_details),
    path("<str:installation>/create/", views.event_create),
    path("<int:event_id>/", views.event_details),
    path("<int:event_id>/update/", views.event_update),
    path("<int:event_id>/delete/", views.event_delete),
]
