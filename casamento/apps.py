# casamento/apps.py
from django.apps import AppConfig

class CasamentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'casamento'

    def ready(self):
        # Importa os sinais quando a app estiver pronta
        import casamento.signals