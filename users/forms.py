from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms

from .models import User


class UserRegistrationForm(UserCreationForm):
    """A form that creates a user, with no privileges, from the given email and password."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example.gmail.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
        }

        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
        }


class ForgotPasswordForm(PasswordResetForm):
    """A form to send a link on password reset to specified email"""
    def clean_email(self):
        """User with specified email must be registered in the system"""
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("The user with this email is not registered.")
        return email


class UserUpdateForm(forms.ModelForm):
    """A form to update user information on the profile page"""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone')

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example.gmail.com', 'class': 'Input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'Input'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'John', 'class': 'Input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe', 'class': 'Input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+(7)1234567890', 'class': 'Input'}),
        }

        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'phone': 'Phone',
        }
