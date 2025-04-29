from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_STAFF = "staff"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_STAFF, "Staff"),
    )

    phone_number = models.CharField(max_length=20, blank=True)
    user_role = models.CharField(
        max_length=16, choices=ROLE_CHOICES, default=ROLE_STAFF
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
