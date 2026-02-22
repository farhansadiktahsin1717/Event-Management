from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .utils import send_activation_email


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name != "users":
        return

    for role_name in ["Admin", "Organizer", "Participant"]:
        Group.objects.get_or_create(name=role_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_activation_email_on_signup(sender, instance, created, **kwargs):
    if created and not instance.is_active and instance.email:
        request = getattr(instance, "_activation_request", None)
        send_activation_email(instance, request=request)
