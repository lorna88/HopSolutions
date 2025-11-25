from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Class representing api application and its configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
