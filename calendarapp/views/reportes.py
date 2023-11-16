from django.http import  JsonResponse
from calendarapp.models.event import Tutoria, OrientacionAcademica, TipoTarea, Tarea,TipoTutoria, DetalleActividadAcademica ,Cita,TipoOrientacionAcademica, EstadoActividadAcademica, EstadoTarea, Motivo, Convocatoria
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from calendarapp.forms import ReportForm
from django.db.models import Q
from accounts.models.user import Persona, Facultad, Materia, FuncionarioDocente



def actualizar_campos_reportes(request):
    
    campo = request.GET.get('campo')
    
    if campo == "facultad":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
                
    elif campo == "materias": 
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
    if campo == "personas":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
                 
    elif campo == 'todos_funcionarios_docentes': 
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
    elif campo == "tipo_tutoria":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")      
            
    elif campo == "tipo_ori_academ":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
    elif campo == "motivos_ori_academ":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    elif campo == "motivo_ori_academ":
        try:
            
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
                 
    if campo == "tipo_tareas":
        try:
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    if campo == "estado_tareas":
        try:
            contador= 0
            queryset= EstadoTarea.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                    if contador == 0:
                        options += f'<option value="">-----------------</option>'
                        options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'
                        options += f'<option value="Vencida">Vencida</option>'  
                        contador += 1
                    else:
                        options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'     
                        contador += 1
        except Exception as e:
            print(f"Se ha producido un error: {e}")
                    
    if campo == "estado_actividades_con_cita":
        try:
            contador= 0
            queryset= EstadoActividadAcademica.objects.exclude(descripcion_estado_actividad_academica='Iniciada')
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                    if contador == 0:
                        options += f'<option value="">-----------------</option>'
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'
                        options += f'<option value="Vencida">Vencida</option>'
                        contador += 1
                    else:
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'   
                        contador += 1
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    if campo == "estado_actividades_sin_cita":
        try:
            contador= 0
            queryset= EstadoActividadAcademica.objects.exclude(descripcion_estado_actividad_academica='Confirmada')
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                    if contador == 0:
                        options += f'<option value="">-----------------</option>'
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'  
                        options += f'<option value="Vencida">Vencida</option>'
                        contador += 1
                    else:
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'     
                    contador += 1
        except Exception as e:
            print(f"Se ha producido un error: {e}")         
        
    if campo == "estado_actividades_all":
        try:
            contador= 0
            queryset= EstadoActividadAcademica.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                    if contador == 0:
                        options += f'<option value="">-----------------</option>'
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>' 
                        options += f'<option value="Vencida">Vencida</option>' 
                        contador += 1
                    else:
                        options += f'<option value="{item.id_estado_actividad_academica}">{item.descripcion_estado_actividad_academica} </option>'     
                        contador += 1
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
    if campo == "convocatoria":
        try:
            
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
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
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
                # else:
                #     #pass
                #     queryset = queryset.exclude(id_cita__isnull=True)
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    #end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(id_tutoria__datetime_inicio_estimado__range=[start_date, end_date]).order_by('-id_tutoria__datetime_inicio_estimado')

                if id_facultad:
                    queryset = queryset.filter(id_tutoria__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_tutoria__id_materia=id_materia)

                if id_funcionario_docente_encargado and id_funcionario_docente_encargado != "":
                    queryset = queryset.filter(id_tutoria__id_funcionario_docente_encargado= id_funcionario_docente_encargado)
                elif id_funcionario_docente_encargado and id_funcionario_docente_encargado == ""  and request.user.is_superuser == False:
                    #obtenemos el funcionario docente que esta solicitando
                    current_user = request.user.id_persona.id
                    #traemos el id del func_doc
                    funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user)
                    queryset = queryset.filter(id_tutoria__id_funcionario_docente_encargado= funcionario_docente)

                if id_estado:
                    if id_estado != 'Vencida':
                        queryset = queryset.filter(id_tutoria__id_estado_actividad_academica=id_estado)
                    else:
                        queryset = queryset.filter(~Q(id_tutoria__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada ', 'Finalizada']), id_tutoria__datetime_fin_estimado__lte= datetime.now())

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
                        id= s.id_cita.id_cita.id_actividad_academica if s.id_cita else s.id_tutoria.id_actividad_academica
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
                            cantidad_participantes,
                            id                              
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
                
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(id_orientacion_academica__datetime_inicio_estimado__range=[start_date, end_date]).order_by('-id_orientacion_academica__datetime_inicio_estimado')
                if id_facultad:
                    queryset = queryset.filter(id_orientacion_academica__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_orientacion_academica__id_materia=id_materia)

                if id_funcionario_docente_encargado and id_funcionario_docente_encargado != "":
                    queryset = queryset.filter(id_orientacion_academica__id_funcionario_docente_encargado= id_funcionario_docente_encargado)
                elif id_funcionario_docente_encargado and id_funcionario_docente_encargado == "" and request.user.is_superuser == False:
                    #obtenemos el funcionario docente que esta solicitando
                    current_user = request.user.id_persona.id
                    #traemos el id del func_doc
                    funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user)
                    queryset = queryset.filter(id_orientacion_academica__id_funcionario_docente_encargado= funcionario_docente)

                if id_estado:
                    if id_estado != 'Vencida':
                        queryset = queryset.filter(id_orientacion_academica__id_estado_actividad_academica=id_estado)
                    else:
                        queryset = queryset.filter(~Q(id_orientacion_academica__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada ', 'Finalizada']), id_orientacion_academica__datetime_fin_estimado__lte= datetime.now())

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
                        id= s.id_cita.id_cita.id_actividad_academica if s.id_cita else s.id_orientacion_academica.id_actividad_academica
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
                            generado_cita, cantidad_participantes,
                            id                            
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
                    #end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(id_cita__datetime_inicio_estimado__range=[start_date, end_date]).order_by('-id_cita__datetime_inicio_estimado')

                if id_facultad:
                    queryset = queryset.filter(id_cita__id_facultad=id_facultad)

                if id_materia:
                    queryset = queryset.filter(id_cita__id_materia=id_materia)

                if id_funcionario_docente_encargado and id_funcionario_docente_encargado != "":
                    queryset = queryset.filter(id_cita__id_funcionario_docente_encargado= id_funcionario_docente_encargado)
                    
                elif id_funcionario_docente_encargado and id_funcionario_docente_encargado == "" and request.user.is_superuser == False:
                    #obtenemos el funcionario docente que esta solicitando
                    current_user = request.user.id_persona.id
                    #traemos el id del func_doc
                    funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user)
                    queryset = queryset.filter(id_cita__id_funcionario_docente_encargado= funcionario_docente)

                if id_estado:
                    if id_estado != 'Vencida':
                        queryset = queryset.filter(id_cita__id_estado_actividad_academica=id_estado)
                    else:
                        queryset = queryset.filter(~Q(id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica__in=['Cancelada ', 'Finalizada']), id_cita__datetime_fin_estimado__lte= datetime.now())

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
                            cantidad_participantes,
                            s.id_cita.id_actividad_academica  
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
    
    
    
class ReporteTareasView(TemplateView):
    template_name = 'calendarapp/reporte_tarea.html'

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
                id_estado_tarea = request.POST.get('id_estado_tarea', '')
                id_tipo_tarea = request.POST.get('id_tipo_tarea', '')
                tipo_actividad = request.POST.get('tipo_actividad', '')
                id_persona_alta= request.POST.get('id_persona_alta', '')
                id_persona_responsable= request.POST.get('id_persona_responsable', '')
                
                # Construcción del queryset
                # Si alguno de los campos no tiene valor, dentro del queryset no se filtran y se obtienen todos los registros que tengan campos 
                
                queryset = Tarea.objects.all()
                
                
                    
                #traemos solo los que no fueron generados por citas
                if tipo_actividad == 'tutoria':
                    #traemos las tareas de tutorias
                    queryset = queryset.filter(id_orientacion_academica= None)
                    if id_facultad:
                        # Obtener las IDs de las tutorías y orientaciones asociadas a la facultad
                        tutoria_ids = Tutoria.objects.filter(id_tutoria__id_facultad=id_facultad).values('id_tutoria')

                        # Filtrar el queryset de Tarea por las IDs combinadas
                        queryset = queryset.filter(id_tutoria__in=tutoria_ids)
                        
                elif tipo_actividad == 'orientacion':
                    #traemos las tareas de orientaciones
                    queryset = queryset.filter(id_tutoria= None)
                    if id_facultad:
                        # Obtener las IDs de las tutorías y orientaciones asociadas a la facultad
                        orientacion_ids = OrientacionAcademica.objects.filter(id_orientacion_academica__id_facultad=id_facultad).values('id_orientacion_academica')
                        
                        # Filtrar el queryset de Tarea por las IDs combinadas
                        queryset = queryset.filter(id_orientacion_academica__in=orientacion_ids)
                else:
                    #traemos todos
                    if id_facultad:
                        # Obtener las IDs de las tutorías y orientaciones asociadas a la facultad
                        tutoria_ids = Tutoria.objects.filter(id_tutoria__id_facultad=id_facultad).values('id_tutoria')
                        orientacion_ids = OrientacionAcademica.objects.filter(id_orientacion_academica__id_facultad=id_facultad).values('id_orientacion_academica')
                        
                        # Filtrar el queryset de Tarea por las IDs combinadas
                        queryset = queryset.filter(Q(id_tutoria__in=tutoria_ids) | Q(id_orientacion_academica__in=orientacion_ids))
                    
                if len(start_date) and len(end_date):
                    # Ajusta las fechas para incluir los registros del día completo
                    #end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(datetime_inicio_estimado__range=[start_date, end_date]).order_by('-datetime_inicio_estimado')            

                if id_estado_tarea:
                    if id_estado_tarea != 'Vencida':
                        queryset = queryset.filter(id_estado_tarea=id_estado_tarea)
                    else:
                        queryset = queryset.filter(~Q(id_estado_tarea__descripcion_estado_tarea__in=['Cancelada', 'Finalizada']), datetime_vencimiento__lte= datetime.now())

                if id_tipo_tarea:
                    queryset = queryset.filter(id_tipo_tarea= id_tipo_tarea)
                    
                if id_persona_responsable:
                    queryset = queryset.filter(id_persona_responsable= id_persona_responsable)
                
                if id_persona_alta and id_persona_alta != "":
                    queryset = queryset.filter(id_persona_alta= id_persona_alta)
                
                elif id_persona_alta and id_persona_alta == "" and request.user.is_superuser == False:
                    #obtenemos la persona que esta solicitando
                    current_user = request.user.id_persona.id
                    queryset = queryset.filter(id_cita__id_funcionario_docente_encargado= current_user)
                    
                #preguntamos si existen registros 
                if queryset.exists():
                    #filtramos solo los campos que nos interesan                                
                    for s in queryset:
                        if s.id_persona_finalizacion:
                            persona_finalizacion= s.id_persona_finalizacion.nombre + ' ' + s.id_persona_finalizacion.apellido
                        else:
                            persona_finalizacion= ''
                        persona_alta= s.id_persona_alta.nombre + ' ' + s.id_persona_alta.apellido
                        if s.id_persona_responsable:
                            persona_responsable= s.id_persona_responsable.nombre + ' ' + s.id_persona_responsable.apellido
                        else: 
                            persona_responsable= ''
                        if s.id_orientacion_academica:
                            id_actividad= s.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                        else:
                            id_actividad= s.id_tutoria.id_tutoria.id_actividad_academica
                        estado_tarea= s.id_estado_tarea.descripcion_estado_tarea
                        tipo_tarea= s.id_tipo_tarea.descripcion_tipo_tarea
                        datetime_inicio_estimado = s.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                        if s.datetime_inicio_real:
                            datetime_inicio_real = s.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            datetime_inicio_real= ''
                        datetime_vencimiento = s.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                        datetime_alta = s.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                        if s.datetime_finalizacion:
                            datetime_finalizacion = s.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            datetime_finalizacion= ''
                        datetime_ultima_modificacion = s.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                        observacion = s.observacion
                        tipo= ''
                        id= ''
                        if s.id_orientacion_academica:
                            id= s.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                            #verificamos si existe en la tabla de cita
                            cita_ori= Cita.objects.filter(id_cita= s.id_orientacion_academica.id_orientacion_academica.id_actividad_academica, es_orientacion_academica= True)
                            if cita_ori.exists():
                                tipo= 'Cita Orientación'
                                
                            else:
                                tipo= 'Orientación'
                        elif s.id_tutoria:
                            id= s.id_tutoria.id_tutoria.id_actividad_academica
                            #verificamos si existe en la tabla de cita
                            cita_tuto= Cita.objects.filter(id_cita= s.id_tutoria.id_tutoria.id_actividad_academica, es_tutoria= True)
                            if cita_tuto.exists():
                                tipo= 'Cita Tutoría'
                            else:
                                tipo= 'Tutoría'
                        
                        data.append([
                            datetime_inicio_estimado,
                            datetime_vencimiento,
                            persona_responsable,
                            tipo_tarea,
                            estado_tarea,
                            persona_alta,
                            datetime_alta,
                            observacion,
                            datetime_inicio_real,
                            datetime_finalizacion,
                            persona_finalizacion,
                            datetime_ultima_modificacion,
                            id_actividad,
                            tipo,
                            id
                        ])
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Tareas'
        context['entity'] = 'Reportes'
        #context['list_url'] = 'reporte/tutoria'
        context['form'] = ReportForm()
        return context