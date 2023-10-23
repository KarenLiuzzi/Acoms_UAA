from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from notify.models import Notification
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
        return self.request.user.notificaciones.all().order_by('-timestamp') #descendente
    
    
    
@login_required
def actualizar_notificacion_leida(request):
    
    campo = request.GET.get('campo')
    
    if campo == "actualizar_notificacion":
        id_notify = request.GET.get('id')
        ins_notificacion = Notification.objects.get(id= id_notify)
        ins_notificacion.read= True
        ins_notificacion.save()
        print(ins_notificacion)
        
    options= {'estado': 'ok'}
    return JsonResponse(options, safe=False)
