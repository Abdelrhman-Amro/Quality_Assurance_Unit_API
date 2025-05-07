import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        PROFESSOR = "PROFESSOR", "Professor"
        TA = "TA", "Teaching Assistant"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, max_length=150)
    role = models.CharField(max_length=10, choices=Role.choices, verbose_name="Role")

    # Fields to use during authentication
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        ordering = ["username"]
        verbose_name = "user"
        verbose_name_plural = "users"
