from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import QuerySet

from users.models import User


class ForUserManager(models.Manager):
    """Manager what automatically filter selecting data by current user."""

    def for_user(self, user: User | AnonymousUser) -> QuerySet:
        """Get a queryset filtered by user."""
        return self.get_queryset().filter(user=user)
