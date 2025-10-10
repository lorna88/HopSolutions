from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('password-reset/', views.ForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('help/', views.HelpView.as_view(), name='help'),
]
