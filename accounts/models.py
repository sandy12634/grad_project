
from django.contrib.auth.models import AbstractUser
from django.db import models

SECTOR_CHOICES = [
    ("sports", "sports"),
    ("health", "health"),
    ("education", "education"),
]

ROLE_CHOICES = [
    ("superadmin", "Super Admin"),
    ("admin", "Admin"),
]

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="admin"
    )
    sector = models.CharField(
        max_length=20,
        choices=SECTOR_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

