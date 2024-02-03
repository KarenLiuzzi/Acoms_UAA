# Django
from django.dispatch import Signal

notificar = Signal(['level', 'destiny', 'actor', 'verbo', 'timestamp', 'tipo', 'id_tipo'])