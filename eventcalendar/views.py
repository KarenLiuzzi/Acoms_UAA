from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from calendarapp.models.event import Cita, Tutoria, OrientacionAcademica, DetalleActividadAcademica
from accounts.models.user import Persona, FuncionarioDocente
from calendarapp.models import Event
from django.forms.models import model_to_dict
from itertools import chain
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
    
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Devuelve un queryset vacío
        return Event.objects.none()

    def get(self, request, *args, **kwargs):
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
        #events = Event.objects.get_all_events(user=request.user)
        events = Event.objects.get_all_events()
        #running_events = Event.objects.get_running_events(user=request.user)
        current_user= request.user
        dict = model_to_dict(current_user)
        ins_persona=  Persona.objects.get(id= dict["id_persona"])
        latest_events = Event.objects.all() #filter(user=request.user).order_by("-id")[:10]
        citas_finalizadas= 0
        citas_confirmadas= 0
        citas_canceladas= 0
        citas_pendientes= 0
        citas_vencidas= 0
        #devolvemos solo aquellos registros que correspondan al usuario logeado
        if current_user.has_perm('calendarapp.iniciar_cita'):
            ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
            #actividades con citas
            citas = Cita.objects.select_related("id_cita").filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
            if citas.exists():
                    for objeto in citas:
                            if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                                objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                                citas_vencidas += 1
                                
                            if objeto.id_cita.datetime_inicio_real:
                                fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_real.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_cita.datetime_inicio_real
                            else:
                                fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                                dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                                dia= dias_semana[dia]
                                horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                                fecha_auxiliar= objeto.id_cita.datetime_inicio_estimado
                            encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                            solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                            
                            estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                            if objeto.es_tutoria== True:
                                tipo= 'Cita Tutoría'
                            elif  objeto.es_orientacion_academica== True:
                                tipo= 'Cita Orientación Académica'
                            id= str(objeto.id_cita.id_actividad_academica)
                            tipo_usuario= 'staff'
                            
                            auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar}                    
                            lista_actividades.append(auxiliar) 
                            
                    
            citas_finalizadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
            citas_confirmadas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Confirmada', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
            citas_canceladas= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Cancelada').count()
            citas_pendientes= citas.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Pendiente', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
           #tutorias sin citas
            tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
            if tutorias.exists():
                        for objeto in tutorias:
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
            #orientaciones sin citas
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
            if orientaciones.exists():
                        for objeto in orientaciones:
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
            #detalle participante
            registros_participante= DetalleActividadAcademica.objects.filter(id_participante= ins_persona).values('id_actividad_academica')
            
            #actividades con citas
            citas_ = Cita.objects.select_related("id_cita").filter(id_cita__id_persona_alta= ins_persona)
            citas_finalizadas_sin_parti= citas_.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
            citas_confirmadas_sin_parti= citas_.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Confirmada', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
            citas_canceladas_sin_parti= citas_.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Cancelada').count()
            citas_pendientes_sin_parti= citas_.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Pendiente', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
            
            citas_participante = Cita.objects.select_related("id_cita").filter(id_cita__id_actividad_academica__in= registros_participante)
            
            if citas_participante.exists():
                citas_finalizadas_parti= citas_participante.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica= 'Finalizada').count()
                citas_confirmadas_parti= citas_participante.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Confirmada', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
                citas_canceladas_parti= citas_participante.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Cancelada').count()
                citas_pendientes_parti= citas_participante.filter(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica=  'Pendiente', id_cita__datetime_fin_estimado__gt= datetime.now()).count()
                #unimos ambos registros 
                citas = citas_.union(citas_participante)
            else:
                citas_finalizadas_parti= 0
                citas_confirmadas_parti= 0
                citas_canceladas_parti= 0
                citas_pendientes_parti= 0
                citas = citas_
            
            if citas.exists():
                    for objeto in citas:
                        if objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica not in ('Finalizada', 'Cancelada', 'Rechazada') and objeto.id_cita.datetime_fin_estimado <= datetime.now():
                            objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica = 'Vencida'
                            citas_vencidas += 1
                            
                        if objeto.id_cita.datetime_inicio_real:
                            fecha= objeto.id_cita.datetime_inicio_real.strftime('%d-%m-%Y')
                            dia= objeto.id_cita.datetime_inicio_real.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_cita.datetime_inicio_real.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_cita.datetime_inicio_real
                        else:
                            fecha= objeto.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
                            dia= objeto.id_cita.datetime_inicio_estimado.weekday()
                            dia= dias_semana[dia]
                            horario= objeto.id_cita.datetime_inicio_estimado.strftime('%H:%M:%S')
                            fecha_auxiliar= objeto.id_cita.datetime_inicio_estimado
                        encargado= str(objeto.id_cita.id_funcionario_docente_encargado)
                        solicitante= objeto.id_cita.id_persona_alta.nombre + ' ' + objeto.id_cita.id_persona_alta.apellido
                        id_solicitante= objeto.id_cita.id_persona_alta.id
                        
                        estado= str(objeto.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                        if objeto.es_tutoria== True:
                            tipo= 'Cita Tutoría'
                        elif  objeto.es_orientacion_academica== True:
                            tipo= 'Cita Orientación Académica'
                        id= str(objeto.id_cita.id_actividad_academica)
                        tipo_usuario= 'normal'
                        
                        auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar, 'id_solicitante': id_solicitante}                    
                        lista_actividades.append(auxiliar) 
                        
                    
            citas_finalizadas= citas_finalizadas_sin_parti + citas_finalizadas_parti
            citas_confirmadas= citas_confirmadas_sin_parti + citas_confirmadas_parti
            citas_canceladas= citas_canceladas_sin_parti + citas_canceladas_parti
            citas_pendientes= citas_pendientes_sin_parti + citas_pendientes_parti
           
            # #tutorias sin citas
            tutorias_ = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_solicitante= ins_persona)
            
            tutorias_participante = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_actividad_academica__in= registros_participante)
            
            if tutorias_participante.exists():
                #unimos ambos registros 
                tutorias = tutorias_.union(tutorias_participante)
            else:
                tutorias = tutorias_
            
            
            if tutorias.exists():
                for objeto in tutorias:                            
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
                    id_solicitante= objeto.id_tutoria.id_persona_solicitante.id
                    
                    estado= str(objeto.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                    tipo= 'Tutoría'
                    id= str(objeto.id_tutoria.id_actividad_academica)
                    tipo_usuario= 'normal'
                    
                    auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar, 'id_solicitante': id_solicitante}                    
                    lista_actividades.append(auxiliar) 
                    
            #orientaciones sin citas
            orientaciones_ = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_solicitante= ins_persona)
            orientaciones_participante = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_actividad_academica__in= registros_participante)
            
            if orientaciones_participante.exists():
                #unimos ambos registros 
                orientaciones = orientaciones_.union(orientaciones_participante)
            else:
                orientaciones = orientaciones_            
            
            if orientaciones.exists():
                for objeto in orientaciones:                                    
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
                        id_solicitante= objeto.id_orientacion_academica.id_persona_solicitante.id
                        estado= str(objeto.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica)
                        tipo= 'Orientación Académica'
                        id= str(objeto.id_orientacion_academica.id_actividad_academica)
                        tipo_usuario= 'normal'
                        
                        auxiliar= {'fecha': fecha, 'dia': dia, 'horario': horario, 'estado': estado, 'encargado': encargado, 'solicitante': solicitante, 'tipo': tipo, 'id': id, 'tipo_usuario': tipo_usuario, 'fecha_auxiliar': fecha_auxiliar, 'id_solicitante': id_solicitante}                    
                        lista_actividades.append(auxiliar) 
    
            running_events = sorted(lista_actividades, key=lambda x: x['fecha_auxiliar'], reverse=True)
            for event in running_events:
                del event['fecha_auxiliar']
                
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
