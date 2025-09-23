from typing import override

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom User model that replaces Django's default User."""

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    @override
    def __str__(self) -> str:
        return self.username
