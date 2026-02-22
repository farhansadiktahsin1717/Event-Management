from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_number_validator = RegexValidator(
    regex=r"^\+?[0-9\s\-()]{7,20}$",
    message="Enter a valid phone number.",
)


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profiles/",
        default="profiles/default_profile.jpg",
        blank=True,
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[phone_number_validator],
        blank=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username
