from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True, max_length=254)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        max_length=128,
        blank=True,
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
