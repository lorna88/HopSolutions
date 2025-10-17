from django.db import models

class ForUserManager(models.Manager):
    """Manager what automatically filter selecting data by current user."""

    def for_user(self, user):
        """Get a queryset filtered by user."""
        return self.get_queryset().filter(user=user)