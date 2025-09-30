from django.contrib import admin
from django.db import models

from subtasks.models import Subtask
from .forms import TaskDateInput
from .models import Category, Task

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1  # Количество пустых форм для добавления новых объектов
    fields = ('name', 'is_completed')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'user', 'is_completed')
    list_per_page = 10

    formfield_overrides = {
        models.DateField: {'widget': TaskDateInput},
    }

    inlines = [SubtaskInline]

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)

    @admin.display(description="Display_tags")
    def display_tags(self, obj: Task) -> str:
        """Отображает теги статьи в списке."""
        # return " %s" % (", ".join(tag.name for tag in obj.tags.all()[:5]))# Ограничиваем для производительности
        return 'dsfsdffg'


admin.site.register(Category)
admin.site.register(Task, TaskAdmin)
