from django.contrib import admin
from django.http import HttpRequest

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Class for representing User model in the admin area"""
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'phone')
    list_per_page = 10
    exclude = ('groups', )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Adding new users is impossible
        It is better to do it with registration form
        """
        return False


admin.site.register(User, UserAdmin)
