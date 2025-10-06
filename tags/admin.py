from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color', 'user')
    list_per_page = 10
    # readonly_fields = ('user',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
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
