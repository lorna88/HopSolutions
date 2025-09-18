from django.contrib.auth import get_user_model
from django.db import models

from tasks.models import Task


class Subtask(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'subtask'
        verbose_name_plural = 'subtasks'

    # def get_absolute_url(self):
    #     return reverse('tasks:task-detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
