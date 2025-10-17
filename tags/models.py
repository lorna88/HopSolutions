from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from tasks.managers import ForUserManager


class Tag(models.Model):
    """Model for tags"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    color = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Attach user manager
    objects = ForUserManager()

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def save(self, *args, **kwargs):
        """
        Fills in the slug field for a new tag.
        The slug consists of name and username
        (to comply with the unique constraint).
        """
        if not self.slug:
            self.slug = slugify(self.name) + '-' + self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
