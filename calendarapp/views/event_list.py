import json
from django.forms import model_to_dict
from django.views.generic import ListView
from django.shortcuts import render
from calendarapp.models import Event
from calendarapp.models.event import Cita, EstadoActividadAcademica,DetalleActividadAcademica, Tutoria, OrientacionAcademica
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        #return Event.objects.get_all_events(user=self.request.user)
        return Event.objects.get_all_events()

class ActividadesAcademicasListView(ListView):
    """ All event list views """

    template_name = "calendarapp/actividades_academicas_list.html"
    model = Event
    context_object_name= "lista_actividades"

    def get_queryset(self):
        #return Event.objects.get_all_events(user=self.request.user)
        return Event.objects.get_all_acti_academ()

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        parametro = self.kwargs['tipo_cita']
        #return Event.objects.get_running_events(user=self.request.user) 
        return Event.objects.get_running_events(tipo_cita= parametro)
    
class RunningActividadesAcademicasListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/actividades_academicas_list.html"
    model = Event
    context_object_name= "lista_actividades"

    def get_queryset(self):
        parametro = self.kwargs['tipo_cita']
        #return Event.objects.get_running_events(user=self.request.user) 
        return Event.objects.get_running_acti_academ(tipo_cita= parametro)

def DetalleCita(request, id_cita):
    cita= Cita.objects.filter(id_cita= id_cita).select_related("id_cita").first()
    #detalles pude enviar uno o varios registros
    detalles= DetalleActividadAcademica.objects.filter(id_actividad_academica= id_cita)
    contexto= {'cita': cita, 'detalles': detalles}
    return render(request,'calendarapp/detalles_cita.html', context= contexto)

def DetalleActividadesAcademicas(request, id_tutoria, id_ori_academ):
    tutoria= []
    orientacion_academica= []
    if id_tutoria > 0:
        tutoria= Tutoria.objects.filter(id_tutoria= id_tutoria).select_related("id_tutoria").first()
        #detalles pude enviar uno o varios registros
        detalles= DetalleActividadAcademica.objects.filter(id_actividad_academica= id_tutoria)
    else:
        orientacion_academica= OrientacionAcademica.objects.filter(id_orientacion_academica= id_ori_academ).select_related("id_orientacion_academica").first()
        #detalles pude enviar uno o varios registros
        detalles= DetalleActividadAcademica.objects.filter(id_actividad_academica= id_ori_academ)
    
    contexto= {'tutoria': tutoria, 'detalles': detalles, 'orientacion_academica': orientacion_academica}
    return render(request,'calendarapp/detalles_actividad_academica.html', context= contexto)

@csrf_exempt
def CancelarCita(request, id_cita):
    if request.method == "POST":
        
            campo = request.POST.get('motivo')
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                
                with transaction.atomic():
                    record = Event.objects.get(id_actividad_academica=id_cita)
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelado').first()
                    record.id_estado_actividad_academica= estado
                    record.save()
                    #motivo_cancelacion
                    record_cita= Cita.objects.get(id_cita= id_cita)
                    record_cita.motivo_cancelacion= campo
                    record_cita.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Cancelada."})})

            except:
                messages.error(request, 'Ocurrió un error al intentar cancelar la cita.')
                
                return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})
    
def CancelarActividadAcademica(request, id_tutoria, id_ori_academ):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                
                if id_tutoria > 0:
                    #obtenemos la instancia de tutoria a cancelar
                    tutoria= Event.objects.get(id_actividad_academica= id_tutoria)
                    print(tutoria)
                    #obtenemos instancia de estado cancelado
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelado').first()
                    tutoria.id_estado_actividad_academica= estado
                    tutoria.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tutoría Cancelada."})})
                else:
                    #obtenemos la instancia de orientacion academica a cancelar
                    orientacion_academica= Event.objects.get(id_actividad_academica= id_ori_academ)
                    #obtenemos instancia de estado cancelado
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelado').first()
                    orientacion_academica.id_estado_actividad_academica= estado
                    orientacion_academica.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Orientación Académica Cancelada."})})
            except:
                messages.error(request, 'Ocurrió un error al intentar cancelar la Actividad Académica.')
                
                return render(request, "calendarapp/cancelar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})
                
    else:
        
        return render(request, "calendarapp/cancelar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})  

def FinalizarActividadAcademica(request, id_tutoria, id_ori_academ):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                
                if id_tutoria > 0:
                    #obtenemos la instancia de tutoria a cancelar
                    tutoria= Event.objects.get(id_actividad_academica= id_tutoria)
                    #obtenemos instancia de estado cancelado
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizado').first()
                    tutoria.id_estado_actividad_academica= estado
                    tutoria.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tutoría Cancelada."})})
                else:
                    #obtenemos la instancia de orientacion academica a cancelar
                    orientacion_academica= Event.objects.get(id_actividad_academica= id_ori_academ)
                    #obtenemos instancia de estado cancelado
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizado').first()
                    orientacion_academica.id_estado_actividad_academica= estado
                    orientacion_academica.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Orientación Académica Cancelada."})})
            except:
                messages.error(request, 'Ocurrió un error al intentar finalizar la Actividad Académica.')
                
                return render(request, "calendarapp/finalizar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})
                
    else:
        
        return render(request, "calendarapp/finalizar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})  
    
        
@csrf_exempt
def AprobarCita(request, id_cita):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                
                    record = Event.objects.get(id_actividad_academica=id_cita)
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Confirmado').first()
                    record.id_estado_actividad_academica= estado
                    record.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Confirmada."})})

            except:
                messages.error(request, 'Ocurrió un error al intentar confirmar la cita.')
                
                return render(request, "calendarapp/confirmar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/confirmar_cita.html", context = {"id_cita": id_cita})