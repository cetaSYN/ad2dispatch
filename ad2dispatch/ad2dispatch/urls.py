from django.contrib import admin
from django.urls import include, path  # url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/profile/', include('userprofiles.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('volunteer/', include('events.urls')),
    path('news/', include('news.urls')),
    path('', include('pages.urls')),
]
# urlpatterns += (url(r'^admin/django-ses/', include('django_ses.urls')),)
