from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'phone')
    list_per_page = 10
    exclude = ('groups', )

    def has_add_permission(self, request):
        """
        Adding new users is impossible
        It is better to do it on registration form
        """
        return False

admin.site.register(User, UserAdmin)
