from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.category_list, name="list"),
    path("create/", views.create_category, name="create"),
    path("<int:pk>/update/", views.update_category, name="update"),
    path("<int:pk>/delete/", views.delete_category, name="delete"),
]
