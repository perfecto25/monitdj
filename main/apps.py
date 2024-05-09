from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    
    def ready(self):
        from .bg_tasks import check_service_active
        check_service_active()

