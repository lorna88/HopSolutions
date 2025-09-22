from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name = 'users/login.html',
        next_page=reverse_lazy('tasks:home'),
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('users:login')), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
]