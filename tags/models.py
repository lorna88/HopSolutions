from django.contrib.auth import get_user_model
from django.db import models

from tasks.managers import ForUserManager


class Tag(models.Model):
    """Model for tags"""
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Attach user manager
    objects = ForUserManager()

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name
