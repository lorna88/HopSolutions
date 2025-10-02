from django.contrib import admin
from django.db import models
from django import forms

from subtasks.models import Subtask
from tags.models import Tag
from .forms import TaskDateInput
from .models import Category, Task
from .widgets import TagSelectMultiple


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1  # Количество пустых форм для добавления новых объектов
    fields = ('name', 'is_completed')


class TaskAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance.user:
                self.fields["category"].queryset = Category.objects.filter(user=self.instance.user)
                self.fields["tags"].queryset = Tag.objects.filter(user=self.instance.user)
        except AttributeError:
            self.instance.user = None


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'date', 'user', 'is_completed')
    fields = ('name', 'slug', 'description', 'category', 'date', 'is_completed', 'tags')
    list_per_page = 10
    # readonly_fields = ('user',)
    form = TaskAdminForm

    formfield_overrides = {
        models.DateField: {'widget': TaskDateInput},
        models.ManyToManyField: {'widget': TagSelectMultiple},
    }

    inlines = [SubtaskInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = Tag.objects.filter(user=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        try:
            if not obj.user:
                obj.user = request.user
        except AttributeError:
            obj.user = request.user

        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_per_page = 10
    # readonly_fields = ('user',)
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        try:
            if not obj.user:
                obj.user = request.user
        except AttributeError:
            obj.user = request.user

        super().save_model(request, obj, form, change)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
