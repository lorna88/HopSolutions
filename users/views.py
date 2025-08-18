
from django.views.generic import CreateView

from .forms import UserRegistrationForm


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'