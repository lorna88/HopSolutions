from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from tasks.models import Task


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    color = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, related_name='tags', blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
