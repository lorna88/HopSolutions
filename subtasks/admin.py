from django.contrib import admin
from django.http import HttpRequest

from .models import Subtask


class SubtaskAdmin(admin.ModelAdmin):
    """Class for representing Subtask model in the admin area"""
    list_display = ('id', 'name', 'slug', 'task', 'user', 'is_completed')
    list_per_page = 10
    readonly_fields = ('user', 'task')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Adding new subtasks is possible on task change page
        """
        return False


admin.site.register(Subtask, SubtaskAdmin)
