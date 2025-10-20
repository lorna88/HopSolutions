from django import forms
from django.contrib import admin
from django.http import HttpRequest

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    """Class for representing Tag model in the admin area"""
    list_display = ('id', 'name', 'color', 'user')
    list_per_page = 10
    # readonly_fields = ('user',)
    exclude = ('user',)

    def save_model(
            self,
            request: HttpRequest,
            obj: Tag,
            form: forms.ModelForm,
            change: bool) -> None:
        """
        Fills in the user field for a new tag.
        Used on add tag form.
        """
        try:
            if not obj.user:
                obj.user = request.user
        except AttributeError:
            obj.user = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Tag, TagAdmin)
