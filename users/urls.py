from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.participant_list, name="list"),
    path("create/", views.create_participant, name="create"),
    path("<int:pk>/update/", views.update_participant, name="update"),
    path("<int:pk>/delete/", views.delete_participant, name="delete"),
]
