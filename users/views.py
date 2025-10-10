from typing import Any

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, \
    LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm, ForgotPasswordForm
from .models import User


class UserCreateView(CreateView):
    """View for creating a new user."""
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        """Display success message if form is valid"""
        messages.success(self.request, 'You have successfully registered in the system!')
        return super().form_valid(form)

    def form_invalid(self, form: UserRegistrationForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        messages.error(self.request, 'The form contains errors. Please check the entered data.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """Display the login form and handle the login action."""
    template_name = 'users/login.html'
    next_page = reverse_lazy('tasks:home')

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        """Display success message if form is valid"""
        user = form.get_user()
        if user.first_name:
            username = user.first_name
        else:
            username = user.username
        messages.success(self.request, f'Welcome, {username}!')
        return super().form_valid(form)

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        messages.error(self.request, 'Incorrect email or password. Please try again.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Log out the user and redirect him on login page."""
    next_page = reverse_lazy('users:login')

    def get_success_url(self) -> str:
        """Display message about having logged out of system"""
        messages.warning(self.request, 'You have logged out of your account.')
        return super().get_success_url()


class ForgotPasswordView(PasswordResetView):
    """Send a link on password reset if the user has forgotten the password"""
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = ForgotPasswordForm

    def form_valid(self, form: ForgotPasswordForm) -> HttpResponse:
        """Display success message if form is valid"""
        messages.success(self.request, 'A password reset link was sent to your Email.')
        return super().form_valid(form)

    def form_invalid(self, form: ForgotPasswordForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        messages.error(self.request, 'Error: Message not sent. Please try again.')
        return super().form_invalid(form)


class ConfirmPasswordView(PasswordResetConfirmView):
    """View for password reset"""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        """Display success message if form is valid"""
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)

    def form_invalid(self, form: SetPasswordForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        messages.error(self.request, 'There are errors when entering a password. Please try again.')
        return super().form_invalid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    """Display the user profile"""
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Set form for user updating into template context"""
        context = super().get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Handle form for user updating"""
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:account')
    template_name = 'users/account.html'

    def form_valid(self, form: UserUpdateForm) -> HttpResponse:
        """Display success message if form is valid"""
        messages.success(self.request, 'Your profile was updated!')
        return super().form_valid(form)

    def form_invalid(self, form: UserUpdateForm) -> HttpResponse:
        """Display error message if there are errors when filling out the form"""
        messages.error(self.request, 'The form contains errors. Please check the entered data.')
        return super().form_invalid(form)


class HelpView(TemplateView):
    """Display the beginner guide and form to send a question for the support service"""
    template_name = 'help.html'
