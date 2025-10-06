from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm, ForgotPasswordForm
from .models import User


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully registered in the system!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'The form contains errors. Please check the entered data.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('tasks:home')

    def form_valid(self, form):
        user = form.get_user()
        if user.first_name:
            username = user.first_name
        else:
            username = user.username
        messages.success(self.request, f'Welcome, {username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect email or password. Please try again.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def get_success_url(self):
        messages.warning(self.request, 'You have logged out of your account.')
        return super().get_success_url()


class ForgotPasswordView(PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        messages.success(self.request, 'A password reset link was sent to your Email.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error: Message not sent. Please try again.')
        return super().form_invalid(form)

class ConfirmPasswordView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There are errors when entering a password. Please try again.')
        return super().form_invalid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:account')
    template_name = 'users/account.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your profile was updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'The form contains errors. Please check the entered data.')
        return super().form_invalid(form)


class HelpView(TemplateView):
    template_name = 'help.html'
