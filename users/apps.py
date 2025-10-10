from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class representing users application and its configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
