from django.contrib import admin

from .models import Subtask


class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task', 'user', 'is_completed')
    list_per_page = 10
    readonly_fields = ('user', 'task')

    def has_add_permission(self, request):
        return False

admin.site.register(Subtask, SubtaskAdmin)
