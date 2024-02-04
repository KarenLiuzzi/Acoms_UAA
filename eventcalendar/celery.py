from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventcalendar.settings')

# Crear una instancia de la aplicación Celery
app = Celery('eventcalendar')

# Cargar la configuración de la aplicación Celery desde la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas en todas las aplicaciones de Django y registra automáticamente
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')