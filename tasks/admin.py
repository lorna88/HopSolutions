from django.contrib import admin
from django.db import models

from subtasks.models import Subtask
from .forms import TaskDateInput
from .models import Category, Task
from .widgets import TagSelectMultiple


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1  # Количество пустых форм для добавления новых объектов
    fields = ('name', 'is_completed')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'user', 'is_completed')
    list_per_page = 10

    formfield_overrides = {
        models.DateField: {'widget': TaskDateInput},
        models.ManyToManyField: {'widget': TagSelectMultiple},
    }

    inlines = [SubtaskInline]


admin.site.register(Category)
admin.site.register(Task, TaskAdmin)
