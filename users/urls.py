from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name = 'users/login.html',
        next_page = reverse_lazy('users:home'),
        redirect_authenticated_user = True
    ), name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
]