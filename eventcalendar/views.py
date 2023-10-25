from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from calendarapp.models.event import Cita, Tutoria, OrientacionAcademica
from accounts.models.user import Persona, FuncionarioDocente
from calendarapp.models import Event
from django.forms.models import model_to_dict
from itertools import chain
from datetime import datetime


# Función para extraer la fecha de cada tipo de objeto
def get_fecha(event):
    if isinstance(event, Cita):
        if event.id_cita.datetime_inicio_real:
            return event.id_cita.datetime_inicio_real
        else:
            return event.id_cita.datetime_inicio_estimado
    elif isinstance(event, Tutoria):
        if event.id_tutoria.datetime_inicio_real:
            return event.id_tutoria.datetime_inicio_real
        else:
            return event.id_tutoria.datetime_inicio_estimado
    elif isinstance(event, OrientacionAcademica):
        if event.id_orientacion_academica.datetime_inicio_real:
            return event.id_orientacion_academica.datetime_inicio_real
        else:
            return event.id_orientacion_academica.datetime_inicio_estimado
class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        #events = Event.objects.get_all_events(user=request.user)
        events = Event.objects.get_all_events()
        #running_events = Event.objects.get_running_events(user=request.user)
        current_user= request.user
        dict = model_to_dict(current_user)
        ins_persona=  Persona.objects.get(id= dict["id_persona"])
        latest_events = Event.objects.all() #filter(user=request.user).order_by("-id")[:10]
        citas_finalizadas= 0
        lista_events= []
        citas_confirmadas= 0
        citas_canceladas= 0
        citas_pendientes= 0
        citas_vencidas= 0
        #devolvemos solo aquellos registros que correspondan al usuario logeado
        if current_user.has_perm('calendarapp.iniciar_cita'):
            ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
            #actividades con citas
            citas = Cita.objects.select_related("id_cita").filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
            for objeto in citas:
                if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                    objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                    citas_vencidas += 1
                    
            citas_finalizadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
            citas_confirmadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Confirmada').count()
            citas_canceladas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Cancelada').count()
            citas_pendientes= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Pendiente', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
           #tutorias sin citas
            tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
            for objeto in tutorias:
                if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                    objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
            #orientaciones sin citas
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
            for objeto in orientaciones:
                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
            
            # Combinar los dos querysets en una sola variable
            lista_events= list(chain(citas, tutorias, orientaciones))
            running_events = sorted(lista_events, key=get_fecha, reverse=True)
        else:
             #actividades con citas
            citas = Cita.objects.select_related("id_cita").filter(id_cita__id_persona_alta= ins_persona)
            for objeto in citas:
                if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                    objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                    citas_vencidas += 1
                    
            citas_finalizadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
            citas_confirmadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Confirmada').count()
            citas_canceladas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Cancelada').count()
            citas_pendientes= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Pendiente', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
           
            # #tutorias sin citas
            tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_alta= ins_persona)
            for objeto in tutorias:
                if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                    objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
            #orientaciones sin citas
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_alta= ins_persona)
            for objeto in orientaciones:
                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
            
            # Combinar los dos querysets en una sola variable
            lista_events= list(chain(citas, tutorias, orientaciones))
            running_events = sorted(lista_events, key=get_fecha, reverse=True)
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "citas_finalizadas": citas_finalizadas,
            "citas_confirmadas": citas_confirmadas,
            "citas_canceladas": citas_canceladas,
            "citas_pendientes": citas_pendientes,      
            "citas_vencidas": citas_vencidas,
        }
        return render(request, self.template_name, context)
