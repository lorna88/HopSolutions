from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return f'tasks/category/{self.slug}/'

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    def get_absolute_url(self):
        return f'tasks/{self.slug}/'

    def __str__(self):
        return self.name