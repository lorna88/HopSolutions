from django import forms

from .models import Task

class TaskDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('is_completed', 'name', 'description', 'date')

        widgets = {
            # 'category': forms.TextInput(attrs={'class': 'Input'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-task-input'}),
            'name': forms.TextInput(attrs={'class': 'InputTask product-name'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Description', 'class': 'InputTask product-description'}),
            'date': TaskDateInput(attrs={'class': 'InputTask form-control author-name'}),
        }
