from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("events.urls", "events"), namespace="events")),
    path(
        "categories/",
        include(("categories.urls", "categories"), namespace="categories"),
    ),
    path("participants/", include(("users.urls", "users"), namespace="users")),
]
