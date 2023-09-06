from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView

from swapper import load_model

Notificacion= load_model('notify', 'Notification')

# Create your views here.

class NotificationList(ListView):
    model= Notificacion
    template_name= 'notify/notificaciones.html'
    context_object_name= 'list_notify'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    #filtramos solo las notificaciones que estan destinadas al usuario logeado
    def get_queryset(self):
        return self.request.user.notificaciones.all()