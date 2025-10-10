from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from tags.models import Tag


class Category(models.Model):
    """Model for categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        """
        Fills in the slug field for a new category.
        The slug consists of name and username
        (to comply with the unique constraint).
        """
        if not self.slug:
            self.slug = slugify(self.name) + '-' + self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Model for tasks"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def get_absolute_url(self):
        """returns URL on page with current task object"""
        return reverse('tasks:task-detail', kwargs={'slug': self.slug})

    @property
    def subtasks_total(self):
        """
        Returns total subtasks count
        Used on list pages
        """
        return self.subtasks.count()

    @property
    def subtasks_completed(self):
        """
        Returns only completed subtasks count
        Used on list pages
        """
        return self.subtasks.filter(is_completed=True).count()

    def save(self, *args, **kwargs):
        """
        Fills in the slug field for a new task.
        The slug consists of name and username
        (to comply with the unique constraint).
        """
        if not self.slug:
            self.slug = slugify(self.name) + '-' + self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
