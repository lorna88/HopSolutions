from django.contrib import admin
from django.db import models

from .forms import TaskDateInput
from .models import Category, Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'user', 'is_completed')
    list_per_page = 10

    formfield_overrides = {
        models.DateField: {"widget": TaskDateInput},
    }


admin.site.register(Category)
admin.site.register(Task, TaskAdmin)
