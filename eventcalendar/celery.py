from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os
from datetime import timedelta
from celery import Celery
#from django.conf import settings
from datetime import timedelta
from celery import schedules

# Establecer la configuración de Django para Celery
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventcalendar.settings')

# Crear una instancia de la aplicación Celery
app = Celery('eventcalendar')
app.conf.update(
    enable_utc = False,
    timezone = 'America/Asuncion',
    broker_url = 'redis://redis:6379/0',
    result_backend = 'db+postgresql://postgres:test@db:5432/AcOMs',
    result_backend_transport_options = {
    'global_keyprefix': 'AcOMs_'
    },   
    broker_connection_retry_on_startup = True,
)

# app.conf.timezone = 'America/Asuncion'
# app.conf.enable_utc = True
# app.conf.broker_url = 'redis://redis:6379/0'
# #app.conf.result_backend = 'redis://redis:6379/0'
# app.conf.result_backend = 'db+postgresql://postgres:test@db:5432/AcOMs'
# app.conf.result_backend_transport_options = {
#     'global_keyprefix': 'AcOMs_'
# }
#app.conf.accept_content = ['json']
# app.conf.beat_schedule = {
#     'say-every-5-seconds': {
#         'task': 'return_something',
#         'schedule': schedules.crontab(minute='*')
#     },
# }


# app.config['CELERYBEAT_SCHEDULE'] = {
#     'say-every-5-seconds': {
#         'task': 'return_something',
#         'schedule': timedelta(seconds=5)
#     },
# }

# Configuración para mantener el comportamiento de reintentos de conexión durante el inicio
# app.conf.broker_connection_retry_on_startup = True
# Cargar la configuración de la aplicación Celery desde la configuración de Django
#app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, return_something.s('hello'), name='add every 10')

    # # Calls test('hello') every 30 seconds.
    # # It uses the same signature of previous task, an explicit name is
    # # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(30.0, return_something.s('hello'), name='add every 30')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, return_hola.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(minute=35, hour=12),
        return_hola.s('Happy Mondays!'),
    )

@app.task(name='return_something')
def return_something(arg):
    print(arg)
    return arg

@app.task(name='return_hola')
def return_hola(arg):
    print  (arg)
    return arg


#app.conf.enable_utc = False
# app.conf.CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Descubre tareas en todas las aplicaciones de Django y registra automáticamente
# app.autodiscover_tasks()

# @app.task(bind=True)# , ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')