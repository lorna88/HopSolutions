from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Class representing tasks application and its configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self) -> None:
        """Runs signals when tasks app starts"""
        import tasks.signals
