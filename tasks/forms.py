from django import forms

from .models import Task, Category


class TaskDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

class TaskUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из аргументов
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=self.instance.user)
            self.fields["category"].empty_label = None

    class Meta:
        model = Task
        fields = ('category', 'is_completed', 'name', 'description', 'date')

        widgets = {
            'category': forms.Select(attrs={'class': 'author-name'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-task-input'}),
            'name': forms.TextInput(attrs={'class': 'InputTaskCard product-name'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Insert your description here...', 'class': 'InputTaskCard product-description'}),
            'date': TaskDateInput(attrs={'class': 'InputTaskCard form-control author-name'}),
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'InputTask', 'placeholder': 'Category name'}),
        }
