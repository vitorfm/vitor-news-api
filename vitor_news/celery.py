import os
from celery import Celery

# Define o settings padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vitor_news.settings')

# Cria a instância do Celery
app = Celery('vitor_news')

# Lê as configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tasks dentro de todos os apps Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
