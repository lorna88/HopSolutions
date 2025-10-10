from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from tasks.models import Task


class Subtask(models.Model):
    """Model for subtasks"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'subtask'
        verbose_name_plural = 'subtasks'

    def save(self, *args, **kwargs):
        """
        Fills in the slug field for a new subtask.
        The slug consists of name and username
        (to comply with the unique constraint).
        """
        user = self.task.user
        self.user = user
        if not self.slug:
            self.slug = slugify(self.name) + '-' + user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
