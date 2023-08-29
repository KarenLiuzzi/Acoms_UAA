from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from calendarapp.models.event import Event, Tutoria, OrientacionAcademica, TipoTarea, TipoTutoria, DetalleActividadAcademica ,Cita,TipoOrientacionAcademica, EstadoActividadAcademica, EstadoTarea, Motivo, Convocatoria
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta, date
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.views.generic import TemplateView
from calendarapp.forms import ReportForm
from django.urls import reverse_lazy
from accounts.models.user import Persona, Departamento, Facultad, Materia, FuncionarioDocente


def actualizar_campos_reportes(request):
    
    campo = request.GET.get('campo')
    
    if campo == "facultad":
        contador= 0
        queryset= ""
        queryset = Facultad.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
                contador += 1
            else:
                options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'  
                contador += 1
                
    elif campo == "materias": 
         # Traer todas las materias 
        contador= 0
        queryset= ""
        queryset = Materia.objects.all()
        
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
                contador += 1
            else:
                options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'     
                contador += 1  
            
    if campo == "personas":
        contador= 0
        queryset= ""
        queryset= Persona.objects.all()
        
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id}">{item.nombre} {item.apellido} {item.documento}</option>'
                contador += 1
            else:
                options += f'<option value="{item.id}">{item.nombre} {item.apellido} {item.documento}</option>'  
                contador += 1
                 
    elif campo == 'todos_funcionarios_docentes':
        contador= 0
        #cambiar  para traer todos los funcionarios_docentes que pertenezcan a un departamento que se encuentre en la facultad seleccionada
        '''
        #pd: descomentar una vez que el modelo de func/doc tenga el campo de departamento
        selected_option = request.GET.get('id_facultad')
        #treaer los departamentos que esten dentro de la facultad
        departamentos =  Departamento.objects.filter(id_facultad= selected_option).values("id_departamento")
        #traer los funcionarios docentes que se encuentren dentro de esos departamentos        
        funcionario_docente=  FuncionarioDocente.objects.filter(id_departamento__in=departamentos).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
        '''
        funcionario_docente=  FuncionarioDocente.objects.all().values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
        queryset= funcionario_docente

        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
                contador += 1
            else:
                options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>' 
                contador += 1
                
    elif campo == "tipo_tutoria":
        contador= 0
        queryset= ""
        queryset = TipoTutoria.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_tipo_tutoria}">{item.descripcion_tipo_tutoria}</option>'
                contador += 1
            else:
                options += f'<option value="{item.id_tipo_tutoria}">{item.descripcion_tipo_tutoria}</option>'  
                contador += 1
                
            
    elif campo == "tipo_ori_academ":
        contador= 0
        queryset= ""
        queryset = TipoOrientacionAcademica.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_tipo_orientacion_academica}">{item.descripcion_tipo_orientacion_academica}</option>'
                contador += 1
            else:
                options += f'<option value="{item.id_tipo_orientacion_academica}">{item.descripcion_tipo_orientacion_academica}</option>'  
                contador += 1
      
        
    elif campo == "motivos_ori_academ":
        contador= 0
        selected_option= ""
        
        queryset= ""
        #traer todos los motivos de acuerdo al tipo de orientacion academica
        queryset = Motivo.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'   
                contador += 1
            else:
                options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'     
                contador += 1
            
    elif campo == "motivo_ori_academ":
        contador= 0
        selected_option= ""
        selected_option = request.GET.get('selected_option')
        
        queryset= ""
        if selected_option != "":
            #traer todos los motivos de acuerdo al tipo de orientacion academica
            queryset = Motivo.objects.filter(id_tipo_orientacion_academica= selected_option)
            # Pasar los datos del queryset a datos HTML
        else:
             queryset = Motivo.objects.all()
             
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'   
                contador += 1
            else:
                options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'     
                contador += 1
                 
    if campo == "tipo_tareas":
        contador= 0
        queryset= TipoTarea.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
                if contador == 0:
                    options += f'<option value="">-----------------</option>'
                    options += f'<option value="{item.id_tipo_tarea}">{item.descripcion_tipo_tarea} </option>'   
                    contador += 1
                else:
                    options += f'<option value="{item.id_tipo_tarea}">{item.descripcion_tipo_tarea} </option>'     
                    contador += 1
            
    if campo == "estado_tareas":
        contador= 0
        queryset= EstadoTarea.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
                if contador == 0:
                    options += f'<option value="">-----------------</option>'
                    options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'  
                    contador += 1
                else:
                    options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'     
                    contador += 1
                    
    if campo == "estado_actividades_con_cita":
        contador= 0
        queryset= EstadoActividadAcademica.objects.exclude(descripcion_estado_actividad_academica='Iniciada')
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
                if contador == 0:
                    options += f'<option value="">-----------------</option>'
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'
                    contador += 1
                else:
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'   
                    contador += 1
    
    if campo == "estado_actividades_sin_cita":
        contador= 0
        queryset= EstadoActividadAcademica.objects.exclude(descripcion_estado_actividad_academica='Confirmado')
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
                if contador == 0:
                    options += f'<option value="">-----------------</option>'
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'  
                    contador += 1
                else:
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'     
                    contador += 1
                    
    if campo == "estado_actividades_all":
        contador= 0
        queryset= EstadoActividadAcademica.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
                if contador == 0:
                    options += f'<option value="">-----------------</option>'
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'  
                    contador += 1
                else:
                    options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'     
                    contador += 1

    if campo == "convocatoria":
        contador= 0
        # Obtén la fecha actual
        queryset= ""
        #traemos la convocatoria actual
        queryset= Convocatoria.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            if contador == 0:
                options += f'<option value="">-----------------</option>'
                options += f'<option value="{item.id_convocatoria}">{item.id_semestre.descripcion_semestre} {item.anho} </option>'
                contador += 1
            else:
                options += f'<option value="{item.id_convocatoria}">{item.id_semestre.descripcion_semestre} {item.anho} </option>'   
                contador += 1
            
    return JsonResponse(options, safe=False)

class ReporteTutoriaView(TemplateView):
    template_name = 'calendarapp/reporte_tutoria.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                id_facultad = request.POST.get('id_facultad', '')
                id_materia = request.POST.get('id_materia', '')
                id_funcionario_docente_encargado = request.POST.get('id_funcionario_docente_encargado', '')
                id_estado = request.POST.get('id_estado', '')
                id_persona_solicitante = request.POST.get('id_persona_solicitante', '')
                id_tipo_tutoria = request.POST.get('id_tipo_tutoria', '')
                cita = request.POST.get('cita', '')
                
                # Construcción del queryset
                # Si alguno de los campos no tiene valor, dentro del queryset no se filtran y se obtienen todos los registros que tengan campos 
                
                queryset = Tutoria.objects.select_related("id_tutoria").all()
                
                #traemos solo los que no fueron generados por citas
                if cita == 'no':
                    #excluimos los que fueron generados por citas
                    queryset = queryset.filter(id_cita= None)
                else:
                    pass
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    queryset = queryset.filter(id_tutoria__datetime_inicio_estimado__range=[start_date, end_date])

                if id_facultad:
                    queryset = queryset.filter(id_tutoria__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_tutoria__id_materia=id_materia)

                if id_funcionario_docente_encargado:
                    queryset = queryset.filter(id_tutoria__id_funcionario_docente_encargado= id_funcionario_docente_encargado)

                if id_estado:
                    queryset = queryset.filter(id_tutoria__id_estado_actividad_academica=id_estado)

                if id_persona_solicitante:
                    queryset = queryset.filter(id_tutoria__id_persona_solicitante=id_persona_solicitante)

                if id_tipo_tutoria:
                    queryset = queryset.filter(id_tipo_tutoria=id_tipo_tutoria)
                
                #preguntamos si existen registros 
                if queryset.exists():
                    #filtramos solo los campos que nos interesan                                
                    for s in queryset:
                        start_estimado = s.id_tutoria.datetime_inicio_estimado.strftime('%d-%m-%Y %H:%M') if s.id_tutoria.datetime_inicio_estimado else ''
                        end_estimado = s.id_tutoria.datetime_fin_estimado.strftime('%d-%m-%Y %H:%M') if s.id_tutoria.datetime_fin_estimado else ''
                        start_real = s.id_tutoria.datetime_inicio_real.strftime('%d-%m-%Y %H:%M') if s.id_tutoria.datetime_inicio_real else ''
                        end_real = s.id_tutoria.datetime_fin_real.strftime('%d-%m-%Y %H:%M') if s.id_tutoria.datetime_fin_real else ''
                        anho_convocatoria = str(s.id_tutoria.id_convocatoria.anho) if s.id_tutoria.id_convocatoria.anho else ''
                        solicitante= s.id_tutoria.id_persona_solicitante.nombre + ' ' + s.id_tutoria.id_persona_solicitante.apellido if s.id_tutoria.id_persona_solicitante else ''
                        generado_cita= 'Si' if s.id_cita else 'No'
                        cantidad_participantes= 0
                        cantidad_participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica = s.id_tutoria.id_actividad_academica).count()
                        if cantidad_participantes > 0 :
                            cantidad_participantes= str(cantidad_participantes)
                        else:
                            cantidad_participantes= '0'
                        data.append([
                            start_estimado + ' - ' + end_estimado,
                            start_real + ' - ' + end_real,
                            s.id_tutoria.id_estado_actividad_academica.descripcion_estado_actividad_academica,
                            s.id_tutoria.id_funcionario_docente_encargado.id_funcionario_docente.nombre + ' ' + s.id_tutoria.id_funcionario_docente_encargado.id_funcionario_docente.apellido,
                            solicitante,
                            s.id_tutoria.id_facultad.descripcion_facultad,
                            s.id_tutoria.id_materia.descripcion_materia,
                            s.id_tutoria.id_convocatoria.id_semestre.descripcion_semestre + ' ' + anho_convocatoria,
                            s.id_tipo_tutoria.descripcion_tipo_tutoria,
                            s.id_tutoria.observacion, 
                            generado_cita,
                            cantidad_participantes                            
                        ])
                    
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Tutorías'
        context['entity'] = 'Reportes'
        #context['list_url'] = 'reporte/tutoria'
        context['form'] = ReportForm()
        return context



class ReporteOrientacionAcademicaView(TemplateView):
    template_name = 'calendarapp/reporte_orientacion_academica.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                id_facultad = request.POST.get('id_facultad', '')
                id_materia = request.POST.get('id_materia', '')
                id_funcionario_docente_encargado = request.POST.get('id_funcionario_docente_encargado', '')
                id_estado = request.POST.get('id_estado', '')
                id_persona_solicitante = request.POST.get('id_persona_solicitante', '')
                id_tipo_orientacion_academica = request.POST.get('id_tipo_orientacion_academica', '')
                id_tipo_motivo = request.POST.get('id_tipo_motivo', '')
                cita = request.POST.get('cita', '')
                
                # Construcción del queryset
                # Si alguno de los campos no tiene valor, dentro del queryset no se filtran y se obtienen todos los registros que tengan campos 
                
                queryset = OrientacionAcademica.objects.select_related("id_orientacion_academica").all()
                
                #traemos solo los que no fueron generados por citas
                if cita == 'no':
                    #excluimos los que fueron generados por citas
                    queryset = queryset.filter(id_cita= None)
                else:
                    pass
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    queryset = queryset.filter(id_orientacion_academica__datetime_inicio_estimado__range=[start_date, end_date])

                if id_facultad:
                    queryset = queryset.filter(id_orientacion_academica__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_orientacion_academica__id_materia=id_materia)

                if id_funcionario_docente_encargado:
                    queryset = queryset.filter(id_orientacion_academica__id_funcionario_docente_encargado= id_funcionario_docente_encargado)

                if id_estado:
                    queryset = queryset.filter(id_orientacion_academica__id_estado_actividad_academica=id_estado)

                if id_persona_solicitante:
                    queryset = queryset.filter(id_orientacion_academica__id_persona_solicitante=id_persona_solicitante)

                if id_tipo_orientacion_academica:
                    queryset = queryset.filter(id_tipo_orientacion_academica=id_tipo_orientacion_academica)
                
                if id_tipo_motivo:
                    queryset = queryset.filter(id_tipo_motivo=id_tipo_motivo)
                
                #preguntamos si existen registros 
                if queryset.exists():
                    #filtramos solo los campos que nos interesan                                
                    for s in queryset:
                        start_estimado = s.id_orientacion_academica.datetime_inicio_estimado.strftime('%d-%m-%Y %H:%M') if s.id_orientacion_academica.datetime_inicio_estimado else ''
                        end_estimado = s.id_orientacion_academica.datetime_fin_estimado.strftime('%d-%m-%Y %H:%M') if s.id_orientacion_academica.datetime_fin_estimado else ''
                        start_real = s.id_orientacion_academica.datetime_inicio_real.strftime('%d-%m-%Y %H:%M') if s.id_orientacion_academica.datetime_inicio_real else ''
                        end_real = s.id_orientacion_academica.datetime_fin_real.strftime('%d-%m-%Y %H:%M') if s.id_orientacion_academica.datetime_fin_real else ''
                        anho_convocatoria = str(s.id_orientacion_academica.id_convocatoria.anho) if s.id_orientacion_academica.id_convocatoria.anho else ''
                        solicitante= s.id_orientacion_academica.id_persona_solicitante.nombre + ' ' + s.id_orientacion_academica.id_persona_solicitante.apellido if s.id_orientacion_academica.id_persona_solicitante else ''
                        generado_cita= 'Si' if s.id_cita else 'No'
                        materia= '' 
                        if s.id_orientacion_academica.id_materia:
                            materia= s.id_orientacion_academica.id_materia.descripcion_materia 
                        else:
                            materia='' 
                            
                        cantidad_participantes= 0
                        cantidad_participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica = s.id_orientacion_academica.id_actividad_academica).count()
                        if cantidad_participantes > 0 :
                            cantidad_participantes= str(cantidad_participantes)
                        else:
                            cantidad_participantes= '0'
                            
                        data.append([
                            start_estimado + ' - ' + end_estimado,
                            start_real + ' - ' + end_real,
                            s.id_orientacion_academica.id_estado_actividad_academica.descripcion_estado_actividad_academica,
                            s.id_orientacion_academica.id_funcionario_docente_encargado.id_funcionario_docente.nombre + ' ' + s.id_orientacion_academica.id_funcionario_docente_encargado.id_funcionario_docente.apellido,
                            solicitante,
                            s.id_orientacion_academica.id_facultad.descripcion_facultad,
                            materia,
                            s.id_orientacion_academica.id_convocatoria.id_semestre.descripcion_semestre + ' ' + anho_convocatoria,
                            s.id_tipo_orientacion_academica.descripcion_tipo_orientacion_academica,
                            s.id_motivo.descripcion_motivo, 
                            s.id_orientacion_academica.observacion,
                            generado_cita, cantidad_participantes                            
                        ])
                    
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Orientaciones Académicas'
        context['entity'] = 'Reportes'
        #context['list_url'] = 'reporte/tutoria'
        context['form'] = ReportForm()
        return context




class ReporteCitasView(TemplateView):
    template_name = 'calendarapp/reporte_citas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                id_facultad = request.POST.get('id_facultad', '')
                id_materia = request.POST.get('id_materia', '')
                id_funcionario_docente_encargado = request.POST.get('id_funcionario_docente_encargado', '')
                id_estado = request.POST.get('id_estado', '')
                id_persona_solicitante = request.POST.get('id_persona_solicitante', '')
                tipo_cita = request.POST.get('tipo_cita', '')
                
                # Construcción del queryset
                # Si alguno de los campos no tiene valor, dentro del queryset no se filtran y se obtienen todos los registros que tengan campos 
                
                queryset = Cita.objects.select_related("id_cita").all()
                
                #traemos solo los que no fueron generados por citas
                if tipo_cita == 'tutoria':
                    #traemos las tutorias
                    queryset = queryset.filter(es_tutoria= True)
                elif tipo_cita == 'orientacion':
                    #traemos las orientaciones
                    queryset = queryset.filter(es_orientacion_academica= True)
                else:
                    #traemos todos
                    pass
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    queryset = queryset.filter(id_cita__datetime_inicio_estimado__range=[start_date, end_date])

                if id_facultad:
                    queryset = queryset.filter(id_cita__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_cita__id_materia=id_materia)

                if id_funcionario_docente_encargado:
                    queryset = queryset.filter(id_cita__id_funcionario_docente_encargado= id_funcionario_docente_encargado)

                if id_estado:
                    queryset = queryset.filter(id_cita__id_estado_actividad_academica=id_estado)

                if id_persona_solicitante:
                    queryset = queryset.filter(id_cita__id_persona_solicitante=id_persona_solicitante)
                
                #preguntamos si existen registros 
                if queryset.exists():
                    #filtramos solo los campos que nos interesan                                
                    for s in queryset:
                        start_estimado = s.id_cita.datetime_inicio_estimado.strftime('%d-%m-%Y %H:%M') if s.id_cita.datetime_inicio_estimado else ''
                        end_estimado = s.id_cita.datetime_fin_estimado.strftime('%d-%m-%Y %H:%M') if s.id_cita.datetime_fin_estimado else ''
                        start_real = s.id_cita.datetime_inicio_real.strftime('%d-%m-%Y %H:%M') if s.id_cita.datetime_inicio_real else ''
                        end_real = s.id_cita.datetime_fin_real.strftime('%d-%m-%Y %H:%M') if s.id_cita.datetime_fin_real else ''
                        anho_convocatoria = str(s.id_cita.id_convocatoria.anho) if s.id_cita.id_convocatoria.anho else ''
                        solicitante= s.id_cita.id_persona_solicitante.nombre + ' ' + s.id_cita.id_persona_solicitante.apellido if s.id_cita.id_persona_solicitante else ''
                        cantidad_participantes= 0
                        cantidad_participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica = s.id_cita.id_actividad_academica).count()
                        if cantidad_participantes > 0 :
                            cantidad_participantes= str(cantidad_participantes)
                        else:
                            cantidad_participantes= '0'
                        tipo= ''
                        if s.es_orientacion_academica == True:
                            tipo= 'Orientación'
                        elif s.es_tutoria == True:
                            tipo= 'Tutoría'
                        materia= '' 
                        if s.id_cita.id_materia:
                            materia= s.id_cita.id_materia.descripcion_materia 
                        else:
                            materia='' 
                        data.append([
                            start_estimado + ' - ' + end_estimado,
                            start_real + ' - ' + end_real,
                            s.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica,
                            s.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.nombre + ' ' + s.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.apellido,
                            solicitante,
                            s.id_cita.id_facultad.descripcion_facultad,
                            materia,
                            s.id_cita.id_convocatoria.id_semestre.descripcion_semestre + ' ' + anho_convocatoria,
                            tipo,
                            s.motivo,
                            s.id_cita.observacion,
                            s.motivo_cancelacion,
                            s.motivo_rechazo,   
                            cantidad_participantes  
                        ])
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Citas'
        context['entity'] = 'Reportes'
        #context['list_url'] = 'reporte/tutoria'
        context['form'] = ReportForm()
        return context