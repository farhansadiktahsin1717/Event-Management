from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
    path("dashboard/", views.DashboardRedirectView.as_view(), name="dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin-dashboard"),
    path("dashboard/participant/", views.ParticipantDashboardView.as_view(), name="participant-dashboard"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="edit-profile"),
    path("profile/change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("participants/", views.participant_list, name="participants"),
    path("participants/<int:pk>/delete/", views.delete_participant, name="participant-delete"),
    path("roles/update/", views.update_user_role, name="update-role"),
    path("groups/create/", views.create_group, name="create-group"),
    path("groups/<int:pk>/delete/", views.delete_group, name="delete-group"),
]
