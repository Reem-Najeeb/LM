from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '_account'
    verbose_name = 'a_الحسابات'

    def ready(self):
        import _account.signals  
        # تأكد من استيراد ملف signals عند بدء تشغيل التطبيق
