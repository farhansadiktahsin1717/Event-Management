from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
    path("dashboard/", views.dashboard_redirect_view, name="dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin-dashboard"),
    path("dashboard/participant/", views.participant_dashboard, name="participant-dashboard"),
    path("participants/", views.participant_list, name="participants"),
    path("participants/<int:pk>/delete/", views.delete_participant, name="participant-delete"),
    path("roles/update/", views.update_user_role, name="update-role"),
    path("groups/create/", views.create_group, name="create-group"),
    path("groups/<int:pk>/delete/", views.delete_group, name="delete-group"),
]
