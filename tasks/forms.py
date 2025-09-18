from django import forms

from .models import Task, Category


class TaskDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('category', 'is_completed', 'name', 'description', 'date')

        widgets = {
            'category': forms.Select(attrs={'class': 'author-name'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-task-input'}),
            'name': forms.TextInput(attrs={'class': 'InputTaskCard product-name'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Description', 'class': 'InputTaskCard product-description'}),
            'date': TaskDateInput(attrs={'class': 'InputTaskCard form-control author-name'}),
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'InputTask', 'placeholder': 'Category name'}),
        }
