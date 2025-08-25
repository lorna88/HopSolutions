from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name = 'users/login.html',
    ), name='login'),
    path('account/', views.AccountView.as_view(), name='account'),
]