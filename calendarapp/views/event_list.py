import json
from django.forms import model_to_dict
from django.views.generic import ListView
from django.shortcuts import render
from calendarapp.models import Event
from calendarapp.models.event import Cita, DetalleActividadAcademica, EstadoActividadAcademica
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        #return Event.objects.get_all_events(user=self.request.user)
        return Event.objects.get_all_events()


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        parametro = self.kwargs['tipo_cita']
        #return Event.objects.get_running_events(user=self.request.user) 
        return Event.objects.get_running_events(tipo_cita= parametro)

def DetalleCita(request, id_cita):
    cita= Cita.objects.filter(id_cita= id_cita).select_related("id_cita").first()
    #detalles pude enviar uno o varios registros
    detalles= DetalleActividadAcademica.objects.filter(id_actividad_academica= id_cita)
    contexto= {'cita': cita, 'detalles': detalles}
    return render(request,'calendarapp/detalles_cita.html', context= contexto)

@login_required
def CancelarCita(request, id_cita):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                record = Event.objects.get(id_actividad_academica=id_cita)
                #indicar aqui el ID correspondiente al 
                estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelado').first()
                record.id_estado_actividad_academica= estado
                record.save()
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Cancelada."})})

            except:
                messages.error(request, 'Ocurrió un error al intentar cancelar la cita.')
                
                return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})