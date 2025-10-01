from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'user')
    list_per_page = 10
    readonly_fields = ('user',)

admin.site.register(Tag, TagAdmin)
