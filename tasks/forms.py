from django import forms

from users.models import User
from .models import Task, Category


class TaskDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('is_completed', 'name', 'description', 'date')

        widgets = {
            # 'category': forms.TextInput(attrs={'class': 'Input'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-task-input'}),
            'name': forms.TextInput(attrs={'class': 'InputTaskCard product-name'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Description', 'class': 'InputTaskCard product-description'}),
            'date': TaskDateInput(attrs={'class': 'InputTaskCard form-control author-name'}),
        }

class TaskCreateForm(forms.ModelForm):
    # def __init__(self, category, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.category = category

    class Meta:
        model = Task
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'InputTask', 'placeholder': 'Add new task'}),
            # 'category': forms.HiddenInput(),
            # 'user': forms.HiddenInput(),
        }

    def save(self, commit=True):
        task = super().save(commit=False)
        category = Category.objects.get(slug='tomorrow')
        task.category = category
        user = User.objects.get(id=1)
        task.user = user
        if commit:
            task.save()
        return task