from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("events/create/", views.create_event, name="create"),
    path("events/<int:pk>/", views.event_detail, name="detail"),
    path("events/<int:pk>/update/", views.update_event, name="update"),
    path("events/<int:pk>/delete/", views.delete_event, name="delete"),
    path("events/<int:pk>/rsvp/", views.rsvp_event, name="rsvp"),
]
