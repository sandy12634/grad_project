from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        # نقوم باستيراد ملف الإشارات من داخل تطبيق الـ dashboard نفسه
        import dashboard.signals