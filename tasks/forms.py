from django import forms
from django.utils.text import slugify

from .models import Task, Category


class TaskDateInput(forms.DateInput):
    """Widget for date input"""
    input_type = 'date'
    format = '%Y-%m-%d'


class TaskUpdateForm(forms.ModelForm):
    """A form to edit task attributes"""
    def __init__(self, *args, **kwargs):
        """
        Filter categories by current user.
        Used on task card form.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.for_user(user)
            self.fields["category"].empty_label = None

    class Meta:
        model = Task
        fields = ('category', 'is_completed', 'name', 'description', 'date')

        widgets = {
            'category': forms.Select(attrs={'class': 'author-name'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'checkbox-task-input'}),
            'name': forms.TextInput(attrs={'class': 'InputTaskCard product-name'}),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Insert your description here...',
                'class': 'InputTaskCard product-description'}),
            'date': TaskDateInput(attrs={'class': 'InputTaskCard form-control author-name'}),
        }


class CategoryCreateForm(forms.ModelForm):
    """A form to create a new category"""
    def __init__(self, *args, **kwargs):
        """
        Add user to form instance
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user

    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'InputTask', 'placeholder': 'Category name'}),
        }

    def clean_name(self):
        """A slug computed by name must be unique for the user"""
        name = self.cleaned_data.get('name')
        slug = slugify(name)
        if Category.objects.for_user(self.instance.user).filter(slug=slug).exists():
            raise forms.ValidationError(f'A category with slug "{slug}" is already exists.')
        return name
