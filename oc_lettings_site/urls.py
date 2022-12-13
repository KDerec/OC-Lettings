from django.contrib import admin
from django.urls import path, include


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sentry-debug/", views.trigger_error),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls),
]
