from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from categories.models import Category
from events.models import Event

from .forms import GroupCreateForm, LoginForm, ProfileUpdateForm, RoleUpdateForm, SignUpForm
from .utils import role_flags_for_user, role_required, user_has_role

User = get_user_model()


def with_role_context(request, context=None):
    base = role_flags_for_user(request.user)
    if context:
        base.update(context)
    return base


class SignupView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = SignUpForm()
        return render(request, "registration/register.html", with_role_context(request, {"form": form}))

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # Pass request through the model instance so signal can build the correct absolute activation URL.
            user._activation_request = request
            user.save()

            participant_group, _ = Group.objects.get_or_create(name="Participant")
            user.groups.add(participant_group)

            messages.success(request, "Account created. Please check your email to activate your account.")
            return redirect("users:login")

        return render(request, "registration/register.html", with_role_context(request, {"form": form}))


def activate_account(request, uidb64, token):
    token = (token or "").replace("\r", "").replace("\n", "").replace(" ", "").replace("=", "")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Your account has been activated. You can now log in.")
    else:
        messages.error(request, "Activation link is invalid or has expired.")

    return redirect("users:login")


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm(request)
        return render(request, "registration/login.html", with_role_context(request, {"form": form}))

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Invalid credentials.")
            elif not user.is_active:
                messages.error(request, "Your account is not activated yet.")
            else:
                login(request, user)
                return redirect("users:dashboard")

        return render(request, "registration/login.html", with_role_context(request, {"form": form}))


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request):
        return redirect("users:dashboard")

    def post(self, request):
        logout(request)
        return redirect("users:login")


@method_decorator(login_required, name="dispatch")
class DashboardRedirectView(View):
    def get(self, request):
        if request.user.is_superuser or user_has_role(request.user, "Admin"):
            return redirect("users:admin-dashboard")
        if user_has_role(request.user, "Organizer"):
            return redirect("events:dashboard")
        return redirect("users:participant-dashboard")


@role_required("Admin")
def admin_dashboard(request):
    users_qs = User.objects.prefetch_related("groups").order_by("username")
    counts = {
        "events": Event.objects.count(),
        "participants": User.objects.filter(groups__name="Participant").distinct().count(),
        "organizers": User.objects.filter(groups__name="Organizer").distinct().count(),
        "categories": Category.objects.count(),
    }

    role_forms = []
    for user in users_qs:
        current_group = user.groups.values_list("name", flat=True).first() or "Participant"
        role_forms.append(
            {
                "user": user,
                "form": RoleUpdateForm(initial={"user_id": user.id, "role": current_group}),
            }
        )

    group_form = GroupCreateForm()
    groups = Group.objects.order_by("name")

    return render(
        request,
        "users/admin_dashboard.html",
        with_role_context(
            request,
            {
                "counts": counts,
                "role_forms": role_forms,
                "group_form": group_form,
                "groups": groups,
            },
        ),
    )


@role_required("Admin")
def update_user_role(request):
    if request.method != "POST":
        return redirect("users:admin-dashboard")

    form = RoleUpdateForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid role update request.")
        return redirect("users:admin-dashboard")

    user = get_object_or_404(User, pk=form.cleaned_data["user_id"])
    role = form.cleaned_data["role"]

    if user == request.user and role != "Admin":
        messages.error(request, "You cannot remove your own admin role.")
        return redirect("users:admin-dashboard")

    group = Group.objects.get(name=role)
    user.groups.clear()
    user.groups.add(group)

    messages.success(request, f"Role for {user.username} updated to {role}.")
    return redirect("users:admin-dashboard")


@role_required("Admin")
def create_group(request):
    if request.method != "POST":
        return redirect("users:admin-dashboard")

    form = GroupCreateForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Group created successfully.")
    else:
        messages.error(request, "Unable to create group.")

    return redirect("users:admin-dashboard")


@role_required("Admin")
def delete_group(request, pk):
    if request.method != "POST":
        return redirect("users:admin-dashboard")

    group = get_object_or_404(Group, pk=pk)
    if group.name in ["Admin", "Organizer", "Participant"]:
        messages.error(request, "Default role groups cannot be deleted.")
        return redirect("users:admin-dashboard")

    group.delete()
    messages.success(request, "Group deleted successfully.")
    return redirect("users:admin-dashboard")


@role_required("Admin")
def participant_list(request):
    participants = (
        User.objects.filter(groups__name="Participant")
        .prefetch_related("rsvp_events")
        .order_by("username")
        .distinct()
    )
    return render(
        request,
        "users/participant_list.html",
        with_role_context(request, {"participants": participants}),
    )


@role_required("Admin")
def delete_participant(request, pk):
    participant = get_object_or_404(User, pk=pk, groups__name="Participant")
    if participant == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("users:participants")

    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
        return redirect("users:participants")

    return render(
        request,
        "users/participant_confirm_delete.html",
        with_role_context(request, {"participant": participant}),
    )


@method_decorator(role_required("Participant", "Admin"), name="dispatch")
class ParticipantDashboardView(View):
    def get(self, request):
        events = request.user.rsvp_events.select_related("category").order_by("date", "time")
        return render(
            request,
            "users/participant_dashboard.html",
            with_role_context(request, {"events": events}),
        )


@method_decorator(login_required, name="dispatch")
class ProfileDetailView(View):
    def get(self, request):
        return render(
            request,
            "users/profile_detail.html",
            with_role_context(request, {"profile_user": request.user}),
        )


@method_decorator(login_required, name="dispatch")
class ProfileEditView(View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(
            request,
            "users/profile_edit.html",
            with_role_context(request, {"form": form}),
        )

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")

        return render(
            request,
            "users/profile_edit.html",
            with_role_context(request, {"form": form}),
        )


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(
            request,
            "users/change_password.html",
            with_role_context(request, {"form": form}),
        )

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("users:profile")

        return render(
            request,
            "users/change_password.html",
            with_role_context(request, {"form": form}),
        )
