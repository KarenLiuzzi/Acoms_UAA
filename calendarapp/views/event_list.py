import json
from django.forms import model_to_dict
from django.views.generic import ListView
from django.shortcuts import render
from accounts.models.user import Persona
from calendarapp.models import Event
from calendarapp.models.event import Cita, EstadoActividadAcademica,DetalleActividadAcademica, Tutoria, OrientacionAcademica, Tarea, EstadoTarea
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from accounts.models.user import FuncionarioDocente
from itertools import chain
from django.db.models import Q,  F, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.utils.decorators import method_decorator


# Función para extraer la fecha de cada tipo de objeto
def get_fecha(event):
    if isinstance(event, Tutoria):
        if event.id_tutoria.datetime_inicio_real:
            return event.id_tutoria.datetime_inicio_real
        else:
            return event.id_tutoria.datetime_inicio_estimado
    elif isinstance(event, OrientacionAcademica):
        if event.id_orientacion_academica.datetime_inicio_real:
            return event.id_orientacion_academica.datetime_inicio_real
        else:
            return event.id_orientacion_academica.datetime_inicio_estimado
        
class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Devuelve un queryset vacío
        return Event.objects.none()
    
    def get_citas(self):
        try:
            lista_eventos= []
            fecha= ''
            dia= ''
            horario= ''
            estado= ''
            encargado= ''
            solicitante= ''
            tipo= '' 
            id= ''
            tipo_usuario= ''
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                event= Event.objects.get_all_events().filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
                # Anotar el queryset con una expresión que determine el campo de ordenamiento
                event = event.annotate(
                    datetime_to_order=Case(
                        When(id_cita__datetime_inicio_real__isnull=False, then=F('id_cita__datetime_inicio_real')),
                        default=F('id_cita__datetime_inicio_estimado')
                    )
                )

                event = event.order_by('-datetime_to_order')
                
                if event.exists():
                    for objeto in event:
                            if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                                objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            if objeto.id_cita.datetime_inicio_real:
                                fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                            else:
                                fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                            encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                            solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                            
                            estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            if objeto.es_tutoria== True:
                                tipo= 'Tutoría'
                            elif  objeto.es_orientacion_academica== True:
                                tipo= 'Orientación Académica'
                            id= str(objeto.id_cita.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario}                    
                            lista_eventos.append(auxiliar) 
                return lista_eventos
                
            else:
                event= Event.objects.get_all_events().filter(id_cita__id_persona_alta= ins_persona)
                # Anotar el queryset con una expresión que determine el campo de ordenamiento
                event = event.annotate(
                    datetime_to_order=Case(
                        When(id_cita__datetime_inicio_real__isnull=False, then=F('id_cita__datetime_inicio_real')),
                        default=F('id_cita__datetime_inicio_estimado')
                    )
                )

                event = event.order_by('-datetime_to_order')
                
                if event.exists():
                    for objeto in event:
                            if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                                objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            if objeto.id_cita.datetime_inicio_real:
                                fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                            else:
                                fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                            encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                            solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                            
                            estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            if objeto.es_tutoria== True:
                                tipo= 'Tutoría'
                            elif  objeto.es_orientacion_academica== True:
                                tipo= 'Orientación Académica'
                            id= str(objeto.id_cita.id_actividad_academica)
                            tipo_usuario= 'normal'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario}                    
                            lista_eventos.append(auxiliar) 
                
                return lista_eventos
                
        except Exception as e:
            print(f"Se ha producido un error en obtener lista de citas: {e}")
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citas'] = self.get_citas()
        return context

class ActividadesAcademicasListView(ListView):
    """ All event list views """

    template_name = "calendarapp/actividades_academicas_list.html"
    model = Event
    
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Devuelve un queryset vacío
        return Event.objects.none()

    def get_actividades(self):
        try:
            lista_actividades= []
            fecha= ''
            dia= ''
            horario= ''
            estado= ''
            encargado= ''
            solicitante= ''
            tipo= '' 
            id= ''
            tipo_usuario= ''
            fecha_auxiliar= ''
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            events= []
            lista_events= []
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
                 
                if tutorias.exists():
                    for objeto in tutorias:
                        if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                            objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                           
                        if objeto.id_tutoria.datetime_inicio_real:
                            fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                            dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                        else:
                            fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                            dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                        encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                        solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                        
                        estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                        tipo= 'Tutoría'
                        id= str(objeto.id_tutoria.id_actividad_academica)
                        tipo_usuario= 'staff'
                        
                        auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                        lista_actividades.append(auxiliar) 
                        
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
                if orientaciones.exists():
                    for objeto in orientaciones:
                            if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                                objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                        
                            if objeto.id_orientacion_academica.datetime_inicio_real:
                                fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                            else:
                                fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                            encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                            solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                            
                            estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            tipo= 'Orientación Académica'
                            id= str(objeto.id_orientacion_academica.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                            
                events = sorted(lista_actividades, key=lambda x: x['fecha_auxiliar'], reverse=True)
                for event in events:
                    del event['fecha_auxiliar']

            else:
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_solicitante= ins_persona)
                if tutorias.exists():
                    for objeto in tutorias:
                        if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                            objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                           
                        if objeto.id_tutoria.datetime_inicio_real:
                            fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                            dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                        else:
                            fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                            dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                        encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                        solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                        
                        estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                        tipo= 'Tutoría'
                        id= str(objeto.id_tutoria.id_actividad_academica)
                        tipo_usuario= 'normal'
                        
                        auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                        lista_actividades.append(auxiliar) 
                        
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_solicitante= ins_persona)
                if orientaciones.exists():
                    for objeto in orientaciones:
                        if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                            objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                    
                        if objeto.id_orientacion_academica.datetime_inicio_real:
                            fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                            dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                        else:
                            fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                            dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                        encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                        solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                        
                        estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                        tipo= 'Orientación Académica'
                        id= str(objeto.id_orientacion_academica.id_actividad_academica)
                        tipo_usuario= 'normal'
                        
                        auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                        lista_actividades.append(auxiliar) 
                    
                events = sorted(lista_actividades, key=lambda x: x['fecha_auxiliar'], reverse=True)
                for event in events:
                    del event['fecha_auxiliar']
                    
                #events = sorted(lista_actividades, key=fecha_auxiliar, reverse=True)
                    
                # Combinar los dos querysets en una sola variable
                # lista_events= list(chain(tutorias, orientaciones))
                # events = sorted(lista_events, key=get_fecha, reverse=True)
            return events
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    def get_actividades_medicion(self):
        data = {}
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            tutoria_iniciada= 0
            tutoria_cancelada= 0
            tutoria_finalizada= 0
            tutoria_vencida= 0
            orientacion_iniciada= 0
            orientacion_cancelada= 0
            orientacion_finalizada= 0
            orientacion_vencida= 0
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
                tutoria_iniciada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_tutoria__datetime_fin_estimado__gt= datetime.now()).count()
                tutoria_cancelada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                tutoria_finalizada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                tutoria_vencida= tutorias.filter(~Q(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_tutoria__datetime_fin_estimado__lte= datetime.now()).count() 
                orientacion_iniciada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_orientacion_academica__datetime_fin_estimado__gt= datetime.now()).count()
                orientacion_cancelada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                orientacion_finalizada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                orientacion_vencida= orientaciones.filter(~Q(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_orientacion_academica__datetime_fin_estimado__lte= datetime.now()).count()  
            else:
                
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_solicitante= ins_persona)
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_solicitante= ins_persona)
                tutoria_iniciada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_tutoria__datetime_fin_estimado__gt= datetime.now()).count()
                tutoria_cancelada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                tutoria_finalizada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                tutoria_vencida= tutorias.filter(~Q(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_tutoria__datetime_fin_estimado__lte= datetime.now()).count() 
                orientacion_iniciada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_orientacion_academica__datetime_fin_estimado__gt= datetime.now()).count()
                orientacion_cancelada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                orientacion_finalizada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                orientacion_vencida= orientaciones.filter(~Q(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_orientacion_academica__datetime_fin_estimado__lte= datetime.now()).count() 
            
            data= {'tutoria_iniciada': tutoria_iniciada, 'tutoria_cancelada': tutoria_cancelada, 'tutoria_finalizada': tutoria_finalizada,
                'orientacion_iniciada': orientacion_iniciada, 'orientacion_cancelada': orientacion_cancelada, 'orientacion_finalizada': orientacion_finalizada, 'tutoria_vencida': tutoria_vencida, 'orientacion_vencida': orientacion_vencida}
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datos'] = self.get_actividades_medicion()
        context['actividades'] = self.get_actividades()
        return context
        

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event
    
    
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Devuelve un queryset vacío
        return Event.objects.none()

    def get_citas(self):
        try:
            lista_eventos= []
            fecha= ''
            dia= ''
            horario= ''
            estado= ''
            encargado= ''
            solicitante= ''
            tipo= '' 
            id= ''
            tipo_usuario= ''
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            parametro = self.kwargs['tipo_cita']
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                event= Event.objects.get_running_events(tipo_cita= parametro).filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
                event = event.annotate(
                    datetime_to_order=Case(
                        When(id_cita__datetime_inicio_real__isnull=False, then=F('id_cita__datetime_inicio_real')),
                        default=F('id_cita__datetime_inicio_estimado')
                    )
                )

                event = event.order_by('-datetime_to_order')
                
                if event.exists():
                    for objeto in event:
                            if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                                objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            if objeto.id_cita.datetime_inicio_real:
                                fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                            else:
                                fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                            encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                            solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                            
                            estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            if objeto.es_tutoria== True:
                                tipo= 'Tutoría'
                            elif  objeto.es_orientacion_academica== True:
                                tipo= 'Orientación Académica'
                            id= str(objeto.id_cita.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario}                    
                            lista_eventos.append(auxiliar) 
                return lista_eventos
            else:
                event= Event.objects.get_running_events(tipo_cita= parametro).filter(id_cita__id_persona_alta= ins_persona)
                event = event.annotate(
                    datetime_to_order=Case(
                        When(id_cita__datetime_inicio_real__isnull=False, then=F('id_cita__datetime_inicio_real')),
                        default=F('id_cita__datetime_inicio_estimado')
                    )
                )

                event = event.order_by('-datetime_to_order')
                
                if event.exists():
                    for objeto in event:
                            if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                                objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            if objeto.id_cita.datetime_inicio_real:
                                fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                            else:
                                fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                            encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                            solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                            
                            estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            if objeto.es_tutoria== True:
                                tipo= 'Tutoría'
                            elif  objeto.es_orientacion_academica== True:
                                tipo= 'Orientación Académica'
                            id= str(objeto.id_cita.id_actividad_academica)
                            tipo_usuario= 'normal'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario}                    
                            lista_eventos.append(auxiliar) 
                return lista_eventos
        #return Event.objects.get_running_events(user=self.request.user) 
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citas'] = self.get_citas()
        return context
        
    
class RunningActividadesAcademicasListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/actividades_academicas_list.html"
    model = Event
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Devuelve un queryset vacío
        return Event.objects.none()

    def get_actividades(self):
        try:
            lista_actividades= []
            fecha= ''
            dia= ''
            horario= ''
            estado= ''
            encargado= ''
            solicitante= ''
            tipo= '' 
            id= ''
            tipo_usuario= ''
            fecha_auxiliar= ''
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            parametro = self.kwargs['tipo_cita']
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            running_events= []
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                if parametro == 'Tutoria':
                    running_events = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
                    if running_events.exists():
                        for objeto in running_events:
                            if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                                objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                            if objeto.id_tutoria.datetime_inicio_real:
                                fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                            else:
                                fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                            encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                            solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                            
                            estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            tipo= 'Tutoría'
                            id= str(objeto.id_tutoria.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                        
                elif parametro== "OriAcademica":
                    running_events = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
                    if running_events.exists():
                        for objeto in running_events:
                                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                                if objeto.id_orientacion_academica.datetime_inicio_real:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                                else:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                                encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                                solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                                
                                estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                                tipo= 'Orientación Académica'
                                id= str(objeto.id_orientacion_academica.id_actividad_academica)
                                tipo_usuario= 'staff'
                                
                                auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                                lista_actividades.append(auxiliar) 
                else: 
                    tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
                    if tutorias.exists():
                        for objeto in tutorias:
                            if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                                objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                            if objeto.id_tutoria.datetime_inicio_real:
                                fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                            else:
                                fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                            encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                            solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                            
                            estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            tipo= 'Tutoría'
                            id= str(objeto.id_tutoria.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                    orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
                    if orientaciones.exists():
                        for objeto in orientaciones:
                                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                                if objeto.id_orientacion_academica.datetime_inicio_real:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                                else:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                                encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                                solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                                
                                estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                                tipo= 'Orientación Académica'
                                id= str(objeto.id_orientacion_academica.id_actividad_academica)
                                tipo_usuario= 'staff'
                                
                                auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                                lista_actividades.append(auxiliar) 
                                
                running_events = sorted(lista_actividades, key=lambda x: x['fecha_auxiliar'], reverse=True)
                for event in running_events:
                    del event['fecha_auxiliar']
                    
            else:
                if parametro == 'Tutoria':
                    running_events = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_solicitante= ins_persona)
                    if running_events.exists():
                        for objeto in running_events:
                            if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                                objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                            if objeto.id_tutoria.datetime_inicio_real:
                                fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                            else:
                                fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                            encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                            solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                            
                            estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            tipo= 'Tutoría'
                            id= str(objeto.id_tutoria.id_actividad_academica)
                            tipo_usuario= 'normal'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                elif parametro== "OriAcademica":
                    running_events = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_solicitante= ins_persona)
                    if running_events.exists():
                        for objeto in running_events:
                                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                                if objeto.id_orientacion_academica.datetime_inicio_real:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                                else:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                                encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                                solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                                
                                estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                                tipo= 'Orientación Académica'
                                id= str(objeto.id_orientacion_academica.id_actividad_academica)
                                tipo_usuario= 'normal'
                                
                                auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                                lista_actividades.append(auxiliar) 
                else: 
                    tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_solicitante= ins_persona)
                    if tutorias.exists():
                        for objeto in tutorias:
                            if objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_tutoria.datetime_fin_estimado <= datetime.now():
                                objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                            if objeto.id_tutoria.datetime_inicio_real:
                                fecha= objeto.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_real
                            else:
                                fecha= objeto.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_tutoria.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_tutoria.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_tutoria.datetime_inicio_estimado
                            encargado= str(objeto.id_tutoria.id_funcionario_docente_encargado)
                            solicitante= objeto.id_tutoria.id_persona_solicitante.nombre + ' ' + objeto.id_tutoria.id_persona_solicitante.apellido
                            
                            estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            tipo= 'Tutoría'
                            id= str(objeto.id_tutoria.id_actividad_academica)
                            tipo_usuario= 'normal'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                    orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_solicitante= ins_persona)
                    if orientaciones.exists():
                        for objeto in orientaciones:
                                if objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_orientacion_academica.datetime_fin_estimado <= datetime.now():
                                    objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            
                                if objeto.id_orientacion_academica.datetime_inicio_real:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_real.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_real.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_real
                                else:
                                    fecha= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                    dia= objeto.id_orientacion_academica.datetime_inicio_estimado.weekday()
                                    dia= dias_semana[dia]
                                    horario= objeto.id_orientacion_academica.datetime_inicio_estimado.strftime('%H:%M:%S')
                                    fecha_auxiliar= objeto.id_orientacion_academica.datetime_inicio_estimado
                                encargado= str(objeto.id_orientacion_academica.id_funcionario_docente_encargado)
                                solicitante= objeto.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + objeto.id_orientacion_academica.id_persona_solicitante.apellido
                                
                                estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                                tipo= 'Orientación Académica'
                                id= str(objeto.id_orientacion_academica.id_actividad_academica)
                                tipo_usuario= 'normal'
                                
                                auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                                lista_actividades.append(auxiliar) 
                                
                running_events = sorted(lista_actividades, key=lambda x: x['fecha_auxiliar'], reverse=True)
                for event in running_events:
                    del event['fecha_auxiliar']
             

            return running_events
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    def get_actividades_medicion(self):
        data = {}
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            parametro = self.kwargs['tipo_cita']
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            tutoria_iniciada= 0
            tutoria_cancelada= 0
            tutoria_finalizada= 0
            tutoria_vencida= 0
            orientacion_iniciada= 0
            orientacion_cancelada= 0
            orientacion_finalizada= 0
            orientacion_vencida= 0
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            if current_user.has_perm('calendarapp.iniciar_cita'):
                ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
                
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
                tutoria_iniciada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_tutoria__datetime_fin_estimado__gt= datetime.now()).count()
                tutoria_cancelada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                tutoria_finalizada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                tutoria_vencida= tutorias.filter(~Q(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_tutoria__datetime_fin_estimado__lte= datetime.now()).count() 
                orientacion_iniciada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_orientacion_academica__datetime_fin_estimado__gt= datetime.now()).count()
                orientacion_cancelada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                orientacion_finalizada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                orientacion_vencida= orientaciones.filter(~Q(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_orientacion_academica__datetime_fin_estimado__lte= datetime.now()).count()  
            else:
                
                tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_alta= ins_persona)
                orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_alta= ins_persona)
                tutoria_iniciada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_tutoria__datetime_fin_estimado__gt= datetime.now()).count()
                tutoria_cancelada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                tutoria_finalizada= tutorias.filter(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                tutoria_vencida= tutorias.filter(~Q(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']), id_tutoria__datetime_fin_estimado__lte= datetime.now()).count() 
                orientacion_iniciada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Iniciada', id_orientacion_academica__datetime_fin_estimado__gt= datetime.now()).count()
                orientacion_cancelada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Cancelada').count()
                orientacion_finalizada= orientaciones.filter(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                orientacion_vencida= orientaciones.filter(~Q(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada', 'Finalizada']) , id_orientacion_academica__datetime_fin_estimado__lte= datetime.now()).count()  
            
            data= {'tutoria_iniciada': tutoria_iniciada, 'tutoria_cancelada': tutoria_cancelada, 'tutoria_finalizada': tutoria_finalizada,
                'orientacion_iniciada': orientacion_iniciada, 'orientacion_cancelada': orientacion_cancelada, 'orientacion_finalizada': orientacion_finalizada, 'tutoria_vencida': tutoria_vencida, 'orientacion_vencida': orientacion_vencida}
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datos'] = self.get_actividades_medicion()
        context['actividades'] = self.get_actividades()
        return context
    
def DetalleCita(request, id_cita):
    try:
        cita= Cita.objects.filter(id_cita= id_cita).select_related("id_cita").first()
        #detalles pude enviar uno o varios registros
        detalles= DetalleActividadAcademica.objects.filter(id_actividad_academica= id_cita)
        contexto= {'cita': cita, 'detalles': detalles}
        return render(request,'calendarapp/detalles_cita.html', context= contexto)
    except Exception as e:
                print(f"Se ha producido un error: {e}")


def DetalleActividadesAcademicas(request, id_tutoria, id_ori_academ):
    try:
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
    except Exception as e:
                print(f"Se ha producido un error: {e}")


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
                dict = model_to_dict(request.user)
                
                with transaction.atomic():
                    record = Event.objects.get(id_actividad_academica=id_cita)
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelada').first()
                    record.id_estado_actividad_academica= estado
                    ins_persona= Persona.objects.get(id= dict["id_persona"])
                    record.id_persona_ultima_modificacion= ins_persona
                    #motivo_cancelacion
                    record_cita= Cita.objects.get(id_cita=id_cita)
                    record_cita.motivo_cancelacion= campo
                    record_cita.save()
                    record.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Cancelada."})})

            except Exception as e:
                print(f"Se ha producido un error: {e}")
                messages.error(request, 'Ocurrió un error al intentar cancelar la cita.')
                return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/cancelar_cita.html", context = {"id_cita": id_cita})
    
        
@csrf_exempt
def AprobarCita(request, id_cita):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                dict = model_to_dict(request.user)
                with transaction.atomic():
                    
                    record = Event.objects.get(id_actividad_academica=id_cita)
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Confirmada').first()
                    record.id_estado_actividad_academica= estado
                    record.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                    record.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Confirmada."})})

            except Exception as e:
                print(f"Se ha producido un error: {e}")
                messages.error(request, 'Ocurrió un error al intentar confirmar la cita.')
                return render(request, "calendarapp/confirmar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/confirmar_cita.html", context = {"id_cita": id_cita})
    
@csrf_exempt
def RechazarCita(request, id_cita):
    if request.method == "POST":
        
            campo = request.POST.get('motivo')
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                dict = model_to_dict(request.user)
                
                with transaction.atomic():
                    record = Event.objects.get(id_actividad_academica=id_cita)
                    estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Rechazada').first()
                    record.id_estado_actividad_academica= estado
                    ins_persona= Persona.objects.get(id= dict["id_persona"])
                    record.id_persona_ultima_modificacion= ins_persona
                    #motivo_cancelacion
                    record_cita= Cita.objects.get(id_cita=id_cita)
                    record_cita.motivo_rechazo= campo
                    record_cita.save()
                    record.save()
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Cita Rechazada."})})

            except Exception as e:
                print(f"Se ha producido un error: {e}")
                messages.error(request, 'Ocurrió un error al intentar rechazar la cita.')
                return render(request, "calendarapp/rechazar_cita.html", context = {"id_cita": id_cita})
                
    else:
        
        return render(request, "calendarapp/rechazar_cita.html", context = {"id_cita": id_cita})

@csrf_exempt
def CancelarActividadAcademica(request, id_tutoria, id_ori_academ):
    if request.method == "POST":

            campo = request.POST.get('motivo')
            
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                dict = model_to_dict(request.user)
                if id_tutoria > 0:
                    with transaction.atomic():
                        #obtenemos la instancia de tutoria a cancelar
                        tutoria= Event.objects.get(id_actividad_academica= id_tutoria)
                        #obtenemos instancia de estado cancelado
                        estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelada').first()
                        tutoria.id_estado_actividad_academica= estado
                        tutoria.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                        hijo_tutoria= Tutoria.objects.get(id_tutoria= id_tutoria)
                        hijo_tutoria.motivo_cancelacion= campo
                        hijo_tutoria.save()
                        tutoria.save()
                        return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tutoría Cancelada."})})
                else:
                    with transaction.atomic():
                        #obtenemos la instancia de orientacion academica a cancelar
                        orientacion_academica= Event.objects.get(id_actividad_academica= id_ori_academ)
                        #obtenemos instancia de estado cancelado
                        estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Cancelada').first()
                        orientacion_academica.id_estado_actividad_academica= estado
                        orientacion_academica.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                        hijo_orientacion= OrientacionAcademica.objects.get(id_orientacion_academica= id_ori_academ)
                        hijo_orientacion.motivo_cancelacion= campo
                        hijo_orientacion.save()
                        orientacion_academica.save()
                        return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Orientación Académica Cancelada."})})
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                messages.error(request, 'Ocurrió un error al intentar cancelar la Actividad Académica.')
                
                return render(request, "calendarapp/cancelar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})
                
    else:
        
        return render(request, "calendarapp/cancelar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})  

@csrf_exempt
def FinalizarActividadAcademica(request, id_tutoria, id_ori_academ):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                
            try:
                dict = model_to_dict(request.user)
                if id_tutoria > 0:
                    with transaction.atomic():
                        #obtenemos la instancia de tutoria a cancelar
                        tutoria= Event.objects.get(id_actividad_academica= id_tutoria)
                        #obtenemos instancia de estado cancelado
                        estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizada').first()
                        tutoria.id_estado_actividad_academica= estado
                        tutoria.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                        tutoria.save()
                        return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tutoría Cancelada."})})
                else:
                    with transaction.atomic():
                        #obtenemos la instancia de orientacion academica a cancelar
                        orientacion_academica= Event.objects.get(id_actividad_academica= id_ori_academ)
                        #obtenemos instancia de estado cancelado
                        estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizada').first()
                        orientacion_academica.id_estado_actividad_academica= estado
                        orientacion_academica.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                        orientacion_academica.save()
                        return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Orientación Académica Cancelada."})})
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                messages.error(request, 'Ocurrió un error al intentar finalizar la Actividad Académica.')
                
                return render(request, "calendarapp/finalizar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})
                
    else:
        
        return render(request, "calendarapp/finalizar_actividad_academica.html", context = {"id_tutoria": id_tutoria, "id_ori_academ": id_ori_academ})  
    

@csrf_exempt
def CancelarTarea(request, id_tarea):
    if request.method == "POST":                
        try:
            with transaction.atomic():
                dict = model_to_dict(request.user)
                record = Tarea.objects.get(id_tarea=id_tarea)
                estado= EstadoTarea.objects.filter(descripcion_estado_tarea='Cancelada').first()
                record.id_estado_tarea= estado
                record.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                record.save()
                # data= json.dumps([{"name": 200}])
                # return HttpResponse(data)
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tarea Cancelada."})})
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            # data= json.dumps([{"name": 500}])
            # return HttpResponse(data)    
            messages.error(request, 'Ocurrió un error al intentar cancelar la Tarea.')
            return render(request, "calendarapp/cancelar_tarea.html", context = {"id_tarea": id_tarea})
                
    else:
        
        return render(request, "calendarapp/cancelar_tarea.html", context = {"id_tarea": id_tarea})  

        
@csrf_exempt
def FinalizarTarea(request, id_tarea):
    if request.method == "POST":                
            try:
                with transaction.atomic():
                    dict = model_to_dict(request.user)
                    record = Tarea.objects.get(id_tarea=id_tarea)
                    estado= EstadoTarea.objects.filter(descripcion_estado_tarea='Finalizada').first()
                    record.id_estado_tarea= estado
                    record.datetime_finalizacion= datetime.now()
                    ins_persona= Persona.objects.get(pk= dict["id_persona"])                
                    record.id_persona_finalizacion= ins_persona
                    record.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                    record.save()
                    # data= json.dumps([{"name": 200}])
                    # return HttpResponse(data)
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tarea Cancelada."})})
        
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                # data= json.dumps([{"name": 500}])
                # return HttpResponse(data)
                messages.error(request, 'Ocurrió un error al intentar finalizar la Tarea.')
                return render(request, "calendarapp/finalizar_tarea.html", context = {"id_tarea": id_tarea})
                
    else:
        
        return render(request, "calendarapp/finalizar_tarea.html", context = {"id_tarea": id_tarea})  
            
@csrf_exempt
def IniciarTarea(request, id_tarea):
    if request.method == "POST":                
            try:
                with transaction.atomic():
                    dict = model_to_dict(request.user)
                    record = Tarea.objects.get(id_tarea=id_tarea)
                    estado= EstadoTarea.objects.filter(descripcion_estado_tarea='Iniciada').first()
                    record.id_estado_tarea= estado
                    record.datetime_inicio_real= datetime.now()
                    record.id_persona_ultima_modificacion= Persona.objects.get(id= dict["id_persona"])
                    record.save()
                    # data= json.dumps([{"name": 200}])
                    # return HttpResponse(data)
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Tarea Cancelada."})})
        
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                # data= json.dumps([{"name": 500}])
                # return HttpResponse(data)
                messages.error(request, 'Ocurrió un error al intentar iniciar la Tarea.')
                return render(request, "calendarapp/iniciar_tarea.html", context = {"id_tarea": id_tarea})
                
    else:
        
        return render(request, "calendarapp/iniciar_tarea.html", context = {"id_tarea": id_tarea})  
                
                
def About(request):
    return render(request,'calendarapp/about.html')