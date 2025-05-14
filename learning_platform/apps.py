from django.apps import AppConfig


class LearningPlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learning_platform'
    verbose_name = 'Образовательная платформа'

    def ready(self):
        """Выполняется при запуске приложения."""
        pass  # Здесь можно добавить инициализацию сигналов или другую логику запуска 