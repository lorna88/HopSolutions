from django.contrib.auth import get_user_model
from django.db import models

from tasks.models import Task


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, related_name='tags', blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    # def get_absolute_url(self):
    #     return reverse('tasks:category', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
