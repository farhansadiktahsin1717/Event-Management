from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def user_has_role(user, *roles):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=roles).exists()


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if user_has_role(request.user, *roles):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this page.")

        return _wrapped_view

    return decorator


def role_flags_for_user(user):
    return {
        "is_admin_user": user_has_role(user, "Admin"),
        "is_organizer_user": user_has_role(user, "Organizer"),
        "is_participant_user": user_has_role(user, "Participant"),
    }


def send_activation_email(user, request=None):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_path = reverse("users:activate", kwargs={"uidb64": uid, "token": token})

    if request is not None:
        activation_url = request.build_absolute_uri(activation_path)
    else:
        activation_url = f"{settings.SITE_URL}{activation_path}"

    send_mail(
        subject="Activate your Event Management account",
        message=(
            f"Hi {user.get_full_name() or user.username},\n\n"
            "Thank you for registering. Please activate your account using the link below:\n"
            f"{activation_url}\n\n"
            "If you did not create this account, please ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
