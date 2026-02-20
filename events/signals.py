from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Event


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    if action != "post_add" or not pk_set:
        return

    user_model = get_user_model()
    recipients = user_model.objects.filter(pk__in=pk_set).exclude(email="")

    for user in recipients:
        send_mail(
            subject=f"RSVP confirmed: {instance.name}",
            message=(
                f"Hello {user.get_full_name() or user.username},\n\n"
                f"Your RSVP for '{instance.name}' on {instance.date} at {instance.time} has been confirmed."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
