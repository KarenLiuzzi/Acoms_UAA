# cal/views.py
import json
from turtle import title
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from calendarapp.mixins import ValidatePermissionRequiredMixin
from calendarapp.models.event import DetalleActividadAcademica
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from calendarapp.forms import HorarioSemestralForm, ActividadAcademicaForm
from accounts.models.user import FuncionarioDocente, Persona, Materia, Departamento, User, Facultad, CarreraAlumno, Carrera,MateriaCarrera
from calendarapp.models import  Event
from calendarapp.models.event import Parametro, Cita, EstadoActividadAcademica, Tutoria, Tarea ,OrientacionAcademica, EstadoTarea ,TipoTutoria, TipoTarea ,TipoOrientacionAcademica, Motivo
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime, timedelta, date
from django.core import serializers
import pandas as pd
from django.db.models import Q

@login_required
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

@login_required
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month

@login_required
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        #events = Event.objects.get_all_events(user=request.user)
        events = Event.objects.get_all_events()
        #events_month = Eveont.objects.get_running_events(user=request.user)
        current_user = request.user
        usuario= model_to_dict(current_user)
        ins_persona= Persona.objects.get(id= usuario["id_persona"])
        tipo_usuario= {}
        #comprobamos que el usuario logeado sea  o funcionario/docente o alumno
        if current_user.has_perm('calendarapp.iniciar_cita'):
            tipo_usuario= {'tipo_usuario': 'staff'}
            #si es funcionario/docente solo pueden ver las citas que fueron asignadas a ellos
            ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
            events= events.filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
        else:
            tipo_usuario= {'tipo_usuario': 'normal'}
            #los que son usuarios normales deben ver solo las citas que fueron generadas por ellos
            #events= events.filter(id_cita__id_persona_solicitante= ins_persona)
            events= events.filter(id_cita__id_persona_alta= ins_persona)
            
        #events_month = Event.objects.get_running_events(tipo_cita= '')
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            tipo_cita= ""
            if event.es_orientacion_academica:
                tipo_cita= "ori_academica"
            elif event.es_tutoria:
                tipo_cita= "tutoria"
                
            #Horario
            horario= ""
            if event.id_cita.datetime_fin_real:
                horario= event.id_cita.datetime_inicio_real.strftime("%H:%M") + ' - ' + event.id_cita.datetime_fin_real.strftime("%H:%M")
            else:
                horario= event.id_cita.datetime_inicio_estimado.strftime("%H:%M") + ' - ' + event.id_cita.datetime_fin_estimado.strftime("%H:%M")
            
            #Fecha
            fecha= ""
            
            if event.id_cita.datetime_inicio_real:
                fecha= event.id_cita.datetime_inicio_real.strftime("%Y-%m-%d")
            else:
                fecha= event.id_cita.datetime_inicio_estimado.strftime("%Y-%m-%d")
                
            #Encargado
            encargado= ""
            #print(type(event.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.nombre))
            encargado= event.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.nombre + ' ' + event.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.apellido
            
            #Receptor
            solicitante= ""
            solicitante= event.id_cita.id_persona_alta.nombre + ' ' + event.id_cita.id_persona_alta.apellido
            
            #Motivo
            motivo= ""
            motivo= event.motivo
            
                
            #Estado
            estado= ""
            estado= event.id_cita.id_estado_actividad_academica.descripcion_estado_actividad_academica
            
            #Convocatoria
            convocatoria= ""
            anho_str= str(event.id_cita.id_convocatoria.anho)
            convocatoria= event.id_cita.id_convocatoria.id_semestre.descripcion_semestre + ' ' + anho_str
            
            #Facultad
            facultad= ""
            
            if event.id_cita.id_facultad:
                facultad= event.id_cita.id_facultad.descripcion_facultad
            else:
                facultad=  "----------"
                
            #Materia
            materia= ""
            if event.id_cita.id_materia:
                materia= event.id_cita.id_materia.descripcion_materia
            else:
                materia= "----------"
            #Observacion
            observacion= ""
            if event.id_cita.observacion:
                observacion= event.id_cita.observacion
            else:
                observacion= "----------"
                
            #Curso
            curso= ""
            
            if event.id_cita.nro_curso:
                curso= event.id_cita.nro_curso
            else:
                curso= "----------"
                
            #tipo 
            tipo=""
            if event.es_orientacion_academica:
                tipo= "Orientacion Académica"
            elif event.es_tutoria:
                tipo= "Tutoría"
            
            #print(tipo)
            
            #Participantes
            #participantes= [{"hola": "karen", "hola2": "liuzzi"}, {"hola": "luis", "hola2": "diaz"}]
            participantes_lista= []
            #print(participantes)
            participantes_filtro= DetalleActividadAcademica.objects.filter(id_actividad_academica= event.id_cita.id_actividad_academica)
            participantes_lista = list(participantes_filtro.values('id_participante__nombre', 'id_participante__apellido'))
            
            if participantes_filtro.exists():
                participantes= participantes_filtro
            else:
                participantes= []
                
            title= ''
            if tipo_usuario['tipo_usuario'] == 'staff':
                title= solicitante
            else: 
                title= encargado
            
            #estos nombres tienen que mantenerse
            event_list.append(
                {
                    "title": title,
                    "start": event.id_cita.datetime_inicio_estimado.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.id_cita.datetime_fin_estimado.strftime("%Y-%m-%dT%H:%M:%S"),
                    "id_cita": event.id_cita.id_actividad_academica,
                    "tipo_cita": tipo_cita,
                    "horario": horario,
                    "fecha": fecha, 
                    "encargado": encargado, 
                    "solicitante": solicitante, 
                    "motivo": motivo, 
                    "estado": estado, 
                    "convocatoria":convocatoria, 
                    "facultad": facultad, 
                    "materia":materia, 
                    "observacion":observacion, 
                    "curso": curso,
                    "tipo": tipo,
                    "participantes": participantes_lista,
                    "tipo_usuario": tipo_usuario['tipo_usuario']
                }
                
            )
            #print(event.id_cita.id_actividad_academica)
        context = {"form": forms, "events": event_list, "tipo_usuario": tipo_usuario}
        return render(request, self.template_name, context)

    #descomentar una vez que este hecho el form de evento
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            #form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
    
#-------------------------------Función ABM Horario Semestral Funcionario/docente------------------------------------
@login_required
def formCalendarioFuncDoc(request):
    try:
        if request.method != "POST":
            
                current_user = request.user
                dict = model_to_dict(current_user)
                persona=  dict["id_persona"]
                dict_cal_fun_doc= HorarioSemestral.objects.filter(id_funcionario_docente= persona)
                context = { "dict_cal_fun_doc": dict_cal_fun_doc}
                return render(request,'calendarapp/calendario_form.html', context= context)
    except Exception as e:
        print(f"Se ha producido un error: {e}")

@login_required
def EditCalendarioFuncDoc(request, pk):
    try:
        hor_sem= get_object_or_404(HorarioSemestral, id_horario_semestral= pk)
        if request.method == "POST":
            #modiicar el form
            form = HorarioSemestralForm(request.POST, instance=hor_sem, user=request.user)
            if form.is_valid():
                form.save()
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro Modificado."})})
            
        else:
            form= HorarioSemestralForm(instance= hor_sem, user=request.user)
        
        #modificar el html
        return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form, "hor_sem": hor_sem})
    except Exception as e:
                print(f"Se ha producido un error: {e}")

@login_required
def AddCalendarioFuncDoc(request):
    try:
        if request.method == "POST":
            form = HorarioSemestralForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro agregado."})})
        else:
            form = HorarioSemestralForm(user=request.user)
        return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form})
    except Exception as e:
            print(f"Se ha producido un error: {e}")

@login_required
def delCalendarioFuncDoc(request, pk):
    if request.method == "POST":
        
            # Eliminar todos los mensajes de error
            storage = messages.get_messages(request)
            for message in storage:
                if message.level == messages.ERROR:
                    storage.discard(message)
                    
            try:
                record = HorarioSemestral.objects.get(id_horario_semestral=pk)
                record.delete()
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro Eliminado."})})

            except Exception as e:
                messages.error(request, f"Ocurrió un error al intentar eliminar el registro. {e}")
                return render(request, "eliminar_registro.html", context = {"pk": pk})
                
    else:
        
        return render(request, "eliminar_registro.html", context = {"pk": pk})


#agregados de pruebas
@login_required
def tipo_cita(request):
    return render(request,'calendarapp/tipo_cita.html')
@login_required
def tipo_acti_academ(request):
    return render(request,'calendarapp/tipo_actividad_academica.html')
@login_required
def ori_academica(request):
    return render(request,'calendarapp/prueba_ori_academica.html')

from django.http import JsonResponse

@csrf_exempt
@login_required
def actualizar_campo(request):
    
    campo = request.GET.get('campo')
    options = ''
    #usado para el alta, modificacion de tutoria y orientacion, inicio de cita tutoria y orientacion
    if campo == "facultad_funcionario":
        try:
            #obtenemos el usuario que solicita
            selected_option = request.user.id_persona
            #traemos el departamento de funcionario
            funcionario_departamento =  FuncionarioDocente.objects.filter(id_funcionario_docente= selected_option).values("id_departamento")
            departamento_facultad= Departamento.objects.filter(id_departamento__in = funcionario_departamento).values("id_facultad")
            
            queryset= ""
            queryset= Facultad.objects.filter(id_facultad__in = departamento_facultad)
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    elif campo == "funcionariodocente_logeado": #usado para el add, modificacion, inicio de de tutoria y orientacion, inicio cita tutoria y orientacion
        try: 
            #obtenemos el usuario que solicita
            current_user = request.user.id_persona
            
            #traemos el id del func_doc
            queryset= ""
            funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
            queryset= funcionario_docente

            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
        
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    elif campo == "funcdoc_logeado_materias": #usado para el add de tutoria, inicio cita tutoria
        try:
            selected_option= ""
            selected_option = request.GET.get('func_doc')
            #obtenemos las materias asignadas al usuario actual
            usuario =  User.objects.filter(id_persona= selected_option).first()
            materias_asignadas = usuario.materia_func_doc.all()
            queryset= Materia.objects.filter(id_materia__in = materias_asignadas)
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    
    if campo == "facultad_alumno": #para alta, edicion de cita tutoria y orientacion
        try:
            #obtenemos el usuario que solicita
            current_user = request.user.id_persona
                
            #Traemos las carreras que esta inscripto el alumno
            carrera_facultad= CarreraAlumno.objects.filter(id_alumno= current_user).values('id_carrera')
            carrera= Carrera.objects.filter(id_carrera__in= carrera_facultad).values('id_facultad')
            facultad_carrera= Facultad.objects.filter(facultad__in= carrera_facultad)
            queryset= ""
            queryset = facultad_carrera
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
    elif campo == "materia": #alta, edicion de cita tutoria
        try:
            '''codigo anterior 
            selected_option= ""
            selected_option = request.GET.get('id_facultad')
            #obtenemos primeramente los Departamentos de la facultad seleccionada
            departamentos =  Departamento.objects.filter(id_facultad= selected_option).values("id_departamento")
            
            # Traer las materias que macheen con los departamentos de la facultad seleccionada
            queryset= ""
            queryset = Materia.objects.filter(id_departamento__in=departamentos)
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
            '''
                
            #codigo nuevo 
            selected_option= ""
            selected_option = request.GET.get('id_facultad')
            
            #obtenemos primeramente los carreras de la facultad seleccionada
            departamentos =  Carrera.objects.filter(id_facultad= selected_option).values("id_carrera")
            
            #obtenemos el usuario que solicita
            current_user = request.user.id_persona
            #Traemos las carreras que esta inscripto el alumno
            carrera_facultad= CarreraAlumno.objects.filter(id_alumno= current_user, id_carrera__in = departamentos).values('id_carrera')
            materias_carrera= MateriaCarrera.objects.filter(id_carrera__in= carrera_facultad).values('id_materia')
            
            #obtener las materias que estan asignadas a esas carreras
            queryset=  Materia.objects.filter(id_materia__in= materias_carrera)
    
             # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'     
            
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    elif campo == "funcionariodocente": #alta, edicion de cita tutoria
        
        try:
            selected_option= ""
            selected_option = request.GET.get('id_materia')
            
            #obtenemos el funcionario docente de la materia seleccionada
            queryset= ""
            #tengo que obtener el id de la materia y traer el usuario que tenga una relacion con esa materia
            materia= Materia.objects.get(id_materia= selected_option)
            usuarios_relacionados= materia.func_doc_materias.all().values('id_persona')
            personas= Persona.objects.filter(id__in= usuarios_relacionados)
            funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente__in=personas).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
            queryset= funcionario_docente

            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                #options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.id_funcionario_docente.nombre} {item.id_funcionario_docente.id_funcionario_docente.apellido}</option>'
                options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
        
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
            
    elif campo == 'todos_funcionarios_docentes_facultad': #para alta, edicion de cita orientacion academica
        #cambiar  para traer todos los funcionarios_docentes que pertenezcan a un departamento que se encuentre en la facultad seleccionada
        try:
            selected_option = request.GET.get('id_facultad')
            #treaer los departamentos que esten dentro de la facultad
            departamentos =  Departamento.objects.filter(id_facultad= selected_option).values("id_departamento")
            #traer los funcionarios docentes que se encuentren dentro de esos departamentos        
            queryset=  FuncionarioDocente.objects.filter(id_departamento__in=departamentos).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                #options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.id_funcionario_docente.nombre} {item.id_funcionario_docente.id_funcionario_docente.apellido}</option>'
                options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
        
        except Exception as e:
            print(f"Se ha producido un error: {e}")
    
    if campo == "facultad": 
        queryset= ""
        queryset = Facultad.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
            
    
    elif campo == 'todos_funcionarios_docentes': #reportes de tutoria, citas, tutoria, orientacion
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
            #options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.id_funcionario_docente.nombre} {item.id_funcionario_docente.id_funcionario_docente.apellido}</option>'
            options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
    
    elif campo == "tipo_tutoria":
        try:
            queryset= ""
            queryset = TipoTutoria.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_tipo_tutoria}">{item.descripcion_tipo_tutoria}</option>'
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    elif campo == "tipo_ori_academ":
        try:
            queryset= ""
            queryset = TipoOrientacionAcademica.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_tipo_orientacion_academica}">{item.descripcion_tipo_orientacion_academica}</option>'
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    elif campo == "motivo_ori_academ":
        try:
            selected_option= ""
            selected_option = request.GET.get('selected_option')
            
            queryset= ""
            #traer todos los motivos de acuerdo al tipo de orientacion academica
            queryset = Motivo.objects.filter(id_tipo_orientacion_academica= selected_option)
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'        
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    elif campo == "materias": #usado en iniciar cita orientacion
        try:
            
            # Traer todas las materias 
            contador= 0
            queryset= ""
            queryset = Materia.objects.all()
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                if contador == 0:
                    options += f'<option value=""></option>'
                    options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
                    contador += 1
                else:
                    options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'     
                    contador += 1  
        except Exception as e:
            print(f"Se ha producido un error: {e}")

    
    if campo == "facultad_func_doc":
        
        #obtenemos el usuario que solicita
        current_user = request.user
        
        #traemos el id del func_doc
        queryset= ""
        #traemos los departamentos del func_doc
        departamentos=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user.id).values('id_departamento').first()
        #traemos las facultades de los departmantos
        facultades= Departamento.objects.filter(id_departamento__in = departamentos).filter("id_facultad").first()
        queryset= ""
        queryset= Facultad.objects.filter(id_facultad= facultades)
        
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
        

    if campo == "convocatoria":
        try:
            # Obtén la fecha actual
            fecha_actual = datetime.now().date()
            queryset= ""
            #traemos la convocatoria actual
            prueba= Convocatoria.objects.filter(id_convocatoria= 1).values('fecha_fin')
            queryset= Convocatoria.objects.filter(fecha_fin__gte = fecha_actual)
            
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_convocatoria}">{item.id_semestre.descripcion_semestre} {item.anho} </option>'
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    if campo == "personas":
        
        try:
            queryset= ""
            queryset= Persona.objects.all()
            
            # Pasar los datos del queryset a datos HTML
            contador = 0
            options = ''
            for item in queryset:
                if contador == 0:
                    options += f'<option value=""></option>'
                    options += f'<option value="{item.id}">{item.nombre} {item.apellido} {item.documento}</option>'
                    contador += 1
                else:
                    options += f'<option value="{item.id}">{item.nombre} {item.apellido} {item.documento}</option>'  
                    contador += 1
        except Exception as e:
            print(f"Se ha producido un error: {e}")      
                 
    if campo == "tipo_tareas":
        try:
            queryset= TipoTarea.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_tipo_tarea}">{item.descripcion_tipo_tarea} </option>'    
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    if campo == "estado_tareas":
        try:
            queryset= EstadoTarea.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = ''
            for item in queryset:
                options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'  
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
    if campo == "estados_tareas":
        try:
            queryset= EstadoTarea.objects.all()
            # Pasar los datos del queryset a datos HTML
            options = []
            for item in queryset:
                estado= item.descripcion_estado_tarea
                id = item.id_estado_tarea
                options.append({"estado": estado, "id": id}) 
        except Exception as e:
            print(f"Se ha producido un error: {e}")
     
    if request.method == "POST":
        accion = request.POST.get('accion')
        descripcion= request.POST.get('descripcion')
        options = []
        if accion == "add_tipo_tutoria":
            try:
                #Primero validamos si ya no existe un tipo de tutoria con la misma descripcion
                queryset= TipoTutoria.objects.filter(descripcion_tipo_tutoria__contains=descripcion)
                if queryset.exists():
                    options.append({"estado": 'existe'}) 
                else:
                    try:
                        ins_tipo_tutoria= TipoTutoria()
                        ins_tipo_tutoria.descripcion_tipo_tutoria= descripcion
                        ins_tipo_tutoria.save()
                        options.append({"estado": 'ok'}) 
                    except Exception as e:
                        print(f"Se ha producido un error: {e}")
                        
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                
        elif accion == "add_tipo_orientacion": 
            try: 
                #Primero validamos si ya no existe un tipo de orientacion con la misma descripcion
                queryset= TipoOrientacionAcademica.objects.filter(descripcion_tipo_orientacion_academica__contains=descripcion)
                if queryset.exists():
                    options.append({"estado": 'existe'}) 
                else:
                    try:
                        ins_tipo_orientacion= TipoOrientacionAcademica()
                        ins_tipo_orientacion.descripcion_tipo_orientacion_academica= descripcion
                        ins_tipo_orientacion.save()
                        options.append({"estado": 'ok'}) 
                    except Exception as e:
                        print(f"Se ha producido un error: {e}")
            except Exception as e:
                print(f"Se ha producido un error: {e}")
                
        elif accion == "add_motivo": 
            try: 
                id_tipo= request.POST.get('id_tipo')
                #Traemos el tipo orientacion
                tipo_orientacion= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica=id_tipo)
                #traemos el motivo
                queryset= Motivo.objects.filter(id_tipo_orientacion_academica= tipo_orientacion, descripcion_motivo__contains= descripcion)
                if queryset.exists():
                    options.append({"estado": 'existe'}) 
                else:
                    try:
                        ins_motivo= Motivo()
                        ins_motivo.descripcion_motivo= descripcion
                        ins_motivo.id_tipo_orientacion_academica= tipo_orientacion
                        ins_motivo.save()
                        options.append({"estado": 'ok'}) 
                    except Exception as e:
                        print(f"Se ha producido un error: {e}")
            except Exception as e:
                print(f"Se ha producido un error: {e}")
            
    return JsonResponse(options, safe=False)

# def obtener_participante(request):
#     documento = request.GET.get('nro_documento')
#     id_persona = request.GET.get('id_persona')
    
#     if id_persona:
#           #obtenemos la persona
#         queryset= ""
#         queryset= Persona.objects.filter(id= id_persona).values("id", "nombre", "apellido")
#         if queryset.count() > 0 :
#             results = list(queryset)
#         else:
#             results= []
        
#     elif documento:
#         #obtenemos el funcionario docente de la materia seleccionada
#         queryset= ""
#         queryset= Persona.objects.filter(documento= documento).values("id", "nombre", "apellido")
#         if queryset.count() > 0:
#             results = list(queryset)
#         else:
#             results= []

#     return JsonResponse(results, safe=False)



#clase de vista de cita de tipo orientacion academica
class CitaOrientacionAcademicaDetalle(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'calendarapp/detalles_cita_orientacion_academica.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'cita'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_cita)
            data= participantes      
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_details_orientacion_academica(self):
        data = OrientacionAcademica.objects.none()
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            orientacion_academica= OrientacionAcademica.objects.filter(id_orientacion_academica=self.get_object().id_cita).first()
            data= orientacion_academica
                    
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_tareas(self):
        data = []
        try:
            tarea= Tarea.objects.filter(id_orientacion_academica= self.get_object().id_cita.id_actividad_academica)
            tareas_lista = list(tarea)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_orientacion_academica = tarea.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_orientacion_academica': id_orientacion_academica, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}  
                    data.append(auxiliar)     
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Cita de Orientación Académica'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['orientacion_academica'] =  self.get_details_orientacion_academica()
        context['tareas'] =  self.get_tareas()
        return context

#clase de vista de cita de tipo tutoria
class CitaTutoriaDetalle(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'calendarapp/detalles_cita_tutoria.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'cita'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_cita)
            data= participantes      
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_details_tutoria(self):
        data = Tutoria.objects.none()
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            tutoria= Tutoria.objects.filter(id_tutoria=self.get_object().id_cita)
            data= tutoria
                    
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_tareas(self):
        data = []
        try:
            tarea= Tarea.objects.filter(id_tutoria= self.get_object().id_cita.id_actividad_academica)
            tareas_lista = list(tarea)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_tutoria = tarea.id_tutoria.id_tutoria.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_tutoria': id_tutoria, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}  
                    data.append(auxiliar)
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Cita de Tutoría'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['tutoria'] =  self.get_details_tutoria()
        context['tareas'] =  self.get_tareas()
        return context  

#clase de vista de tipo orientacion academica
class OrientacionAcademicaDetalle(LoginRequiredMixin, DetailView):
    model = OrientacionAcademica
    template_name = 'calendarapp/detalles_orientacion_academica.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'orientacion_academica'
    queryset= OrientacionAcademica.objects.select_related("id_orientacion_academica")
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_tareas(self):
        data = []
        try:
            tarea= Tarea.objects.filter(id_orientacion_academica= self.get_object())
            tareas_lista = list(tarea)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_orientacion_academica = tarea.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_orientacion_academica': id_orientacion_academica, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}  
                    data.append(auxiliar)     
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_orientacion_academica)
            data= participantes      
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Orientación Académica'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['tareas'] =  self.get_tareas()
        return context
    

#clase de vista de tipo tutoria 
class TutoriaDetalle(LoginRequiredMixin, DetailView):
    model = Tutoria
    template_name = 'calendarapp/detalles_tutoria.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'tutoria'
    queryset= Tutoria.objects.select_related("id_tutoria")
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_tareas(self):
        data = []
        try:
            tarea= Tarea.objects.filter(id_tutoria= self.get_object())
            tareas_lista = list(tarea)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_tutoria = tarea.id_tutoria.id_tutoria.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_tutoria': id_tutoria, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}  
                    data.append(auxiliar)
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        
        return data
    
    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_tutoria)
            data= participantes
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_ins_event(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            event= Event.objects.get(id_actividad_academica= self.get_object().id_tutoria.id_actividad_academica)
            data= event      
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Tutoría'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['tareas'] =  self.get_tareas()
        context['event'] =  self.get_ins_event()
        return context

#clase de creacion para una cita de tipo tutoria
class CitaTutoriaCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/cita_tutoria_create.html'
    success_url = 'running-event-list/tutoria/' #reverse_lazy('calendarapp:calenders')
    #permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'add':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='pendiente').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%d-%m-%Y %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%d-%m-%Y %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_convocatoria = ins_convocatoria
                    cita.id_facultad= ins_facultad
                    cita.id_materia= ins_materia
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.id_persona_alta= ins_persona
                    cita.id_persona_solicitante= ins_persona
                    cita.id_persona_ultima_modificacion= ins_persona
                    cita.datetime_inicio_estimado= fecha_hora_inicio
                    cita.datetime_fin_estimado= fecha_hora_fin
                    cita.nro_curso= actividad_academica['nro_curso']
                    cita.datetime_registro= datetime.now()
                    cita.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita()
                    cita_hijo.id_cita= ins_actividad_academica
                    cita_hijo.es_tutoria= True
                    #traemos el parametro actual 
                    id_parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minuto').first()
                    cita_hijo.id_parametro= id_parametro
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print('aqui')
            #probar
        return JsonResponse(data, safe=False) #, json_dumps_params=[{"showMessage": "Registro Guardado."}]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solicitud de una Cita para Tutoría'
        context['entity'] = 'Tutoría'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

#clase de creacion para una cita de tipo Orientacion Academica
class CitaOrientacionAcademicaCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/cita_orientacion_academica_create.html'
    success_url = 'running-event-list/orientacionAcademica/' #reverse_lazy('calendarapp:calenders')
    #permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'add':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='pendiente').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica actual
                    ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    ''' con la logica posterior
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento'"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    '''
        
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%d-%m-%Y %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%d-%m-%Y %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_convocatoria = ins_convocatoria
                    cita.id_facultad= ins_facultad
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.id_persona_alta= ins_persona
                    cita.id_persona_solicitante= ins_persona
                    cita.id_persona_ultima_modificacion= ins_persona
                    cita.datetime_inicio_estimado= fecha_hora_inicio
                    cita.datetime_fin_estimado= fecha_hora_fin
                    cita.nro_curso= actividad_academica['nro_curso']
                    cita.datetime_registro= datetime.now()
                    cita.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita()
                    cita_hijo.id_cita= ins_actividad_academica
                    cita_hijo.es_orientacion_academica= True
                    #traemos el parametro actual 
                    id_parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minuto').first()
                    cita_hijo.id_parametro= id_parametro
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solicitud de una Cita para Orientación Académica'
        context['entity'] = 'Orientación Academica'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

#Clase de editar de una cita tipo Tutoria
class CitaTutoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/cita_tutoria_edit.html'
    success_url = 'running-event-list/tutoria/'
    #permission_required = 'erp.change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='pendiente').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%d-%m-%Y %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%d-%m-%Y %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_convocatoria = ins_convocatoria
                    cita.id_facultad= ins_facultad
                    cita.id_materia= ins_materia
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.id_persona_ultima_modificacion= ins_persona
                    #cita.id_persona_alta= ins_persona
                    cita.datetime_inicio_estimado= fecha_hora_inicio
                    cita.datetime_fin_estimado= fecha_hora_fin
                    cita.nro_curso= actividad_academica['nro_curso']
                    cita.save()
                    
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita.objects.get(id_cita= ins_actividad_academica)
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_datos_cita(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ, incluido el campo de motivo de la tabla cita
            ins_cita = Cita.objects.filter(id_cita= self.get_object().id_actividad_academica).select_related("id_cita")
            for item in ins_cita:
                id_facultad= item.id_cita.id_facultad.id_facultad
                id_funcionario_docente_encargado= item.id_cita.id_funcionario_docente_encargado
                #traemos solo el id del func_doc
                id_funcionario_docente_encargado= list(FuncionarioDocente.objects.filter(id_funcionario_docente= id_funcionario_docente_encargado).values('id_funcionario_docente'))[0]['id_funcionario_docente']
                id_materia= item.id_cita.id_materia.id_materia
                nro_curso= item.id_cita.nro_curso
                motivo= item.motivo
                auxiliar= {'id_facultad': id_facultad, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 'id_materia': id_materia, 'nro_curso': nro_curso, 'motivo': motivo}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_datos_horario(self):
        data = []
        try:
            # Mapear el número de mes al nombre en español
            meses_espanol = {
                'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
                'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
            }

            dias_espanol = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado'
            }
            
            cita= Event.objects.get(id_actividad_academica=self.get_object().id_actividad_academica)
            fecha= cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
            hora_inicio= cita.datetime_inicio_estimado.strftime('%H:%M:%S')
            hora_fin= cita.datetime_fin_estimado.strftime('%H:%M:%S')
            dia= dias_espanol[cita.datetime_inicio_estimado.strftime('%A')]
            convo= cita.id_convocatoria.id_convocatoria
            mes= meses_espanol[cita.datetime_inicio_estimado.strftime('%B')]
            
            data.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convo, "mes": mes})
            
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Cita de Tutoría'
        context['entity'] = 'Tutoría'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_participantes())
        context['horario'] = json.dumps(self.get_datos_horario())
        context['cita'] = json.dumps(self.get_datos_cita())
        return context

#Clase de editar de una cita tipo Orientacion Academica
class CitaOrientacionAcademicaUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/cita_orientacion_academica_edit.html'
    success_url = 'running-event-list/orientacionAcademica/'
    #permission_required = 'erp.change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='pendiente').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica actual
                    ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    ''' con la logica posterior
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento'"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    '''
        
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%d-%m-%Y %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%d-%m-%Y %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_convocatoria = ins_convocatoria
                    cita.id_facultad= ins_facultad
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.id_persona_ultima_modificacion= ins_persona
                    #cita.id_persona_alta= ins_persona
                    cita.datetime_inicio_estimado= fecha_hora_inicio
                    cita.datetime_fin_estimado= fecha_hora_fin
                    cita.nro_curso= actividad_academica['nro_curso']
                    cita.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita.objects.get(id_cita= ins_actividad_academica)
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                    
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()                    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_datos_cita(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ, incluido el campo de motivo de la tabla cita
            ins_cita = Cita.objects.filter(id_cita= self.get_object().id_actividad_academica).select_related("id_cita")
            for item in ins_cita:
                id_facultad= item.id_cita.id_facultad.id_facultad
                id_funcionario_docente_encargado= item.id_cita.id_funcionario_docente_encargado
                #traemos solo el id del func_doc
                id_funcionario_docente_encargado= list(FuncionarioDocente.objects.filter(id_funcionario_docente= id_funcionario_docente_encargado).values('id_funcionario_docente'))[0]['id_funcionario_docente']
                nro_curso= item.id_cita.nro_curso
                motivo= item.motivo
                auxiliar= {'id_facultad': id_facultad, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 'nro_curso': nro_curso, 'motivo': motivo}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_datos_horario(self):
        data = []
        try:
            # Mapear el número de mes al nombre en español
            meses_espanol = {
                'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
                'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
            }

            dias_espanol = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado'
            }
            
            cita= Event.objects.get(id_actividad_academica=self.get_object().id_actividad_academica)
            fecha= cita.datetime_inicio_estimado.strftime('%d-%m-%Y')
            hora_inicio= cita.datetime_inicio_estimado.strftime('%H:%M:%S')
            hora_fin= cita.datetime_fin_estimado.strftime('%H:%M:%S')
            dia= dias_espanol[cita.datetime_inicio_estimado.strftime('%A')]
            convo= cita.id_convocatoria.id_convocatoria
            mes= meses_espanol[cita.datetime_inicio_estimado.strftime('%B')]
            
            data.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convo, "mes": mes})
            
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Cita de Orientación Académica'
        context['entity'] = 'Orientación Académica'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_participantes())
        context['horario'] = json.dumps(self.get_datos_horario())
        context['cita'] = json.dumps(self.get_datos_cita())
        return context  


#Clase de ininciar una cita tipo Tutoria
class CitaTutoriaIniciarView(LoginRequiredMixin, ValidatePermissionRequiredMixin ,UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/iniciar_cita_tutoria.html'
    success_url = 'running-event-list/tutoria/'
    permission_required = 'calendarapp.iniciar_cita'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'iniciar':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizado').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio_real = datetime.strptime(actividad_academica['datetime_inicio_real'], "%Y-%m-%d %H:%M:%S")
                    fecha_hora_fin_real = datetime.strptime(actividad_academica['datetime_fin_real'], "%Y-%m-%d %H:%M:%S")
                    #obtener las instancias de los objectos 
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_facultad= ins_facultad
                    cita.id_materia= ins_materia
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.datetime_inicio_real= fecha_hora_inicio_real
                    cita.datetime_fin_real = fecha_hora_fin_real
                    dict = model_to_dict(request.user)
                    cita.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    cita.nro_curso= actividad_academica['nro_curso']
                    cita.observacion= actividad_academica['observacion']
                    cita.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita.objects.get(id_cita= ins_actividad_academica)
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                        
                    #guardar datos de la tutoria
                    tutoria= Tutoria()
                    #traer ins de cita
                    ins_cita= Cita.objects.get(id_cita= self.get_object().id_actividad_academica)
                    tutoria.id_tutoria= ins_actividad_academica
                    tutoria.id_cita= ins_cita
                    ins_tipo_tutoria= TipoTutoria.objects.get(id_tipo_tutoria= actividad_academica['id_tipo_tutoria'])
                    tutoria.id_tipo_tutoria= ins_tipo_tutoria
                    tutoria.nombre_trabajo = actividad_academica['nombre_trabajo_grado']
                    tutoria.save()
                    
                    if actividad_academica['tareas']:
                        #obtenemos la persona que esta dando de alta 
                                current_user = request.user
                                dict = model_to_dict(current_user)
                                id_persona=  dict["id_persona"]
                                ins_persona= Persona.objects.get(id= id_persona)
                                for i in actividad_academica['tareas']:
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_tutoria= tutoria
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada, agregar quien finalizo
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                    
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.observacion=  i['observacion']
                                    tarea.save()
                                                        
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_datos_cita(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ, incluido el campo de motivo de la tabla cita
            ins_cita = Cita.objects.filter(id_cita= self.get_object().id_actividad_academica).select_related("id_cita")
            for item in ins_cita:
                id_facultad= item.id_cita.id_facultad.id_facultad
                id_funcionario_docente_encargado= item.id_cita.id_funcionario_docente_encargado
                #traemos solo el id del func_doc
                id_funcionario_docente_encargado= list(FuncionarioDocente.objects.filter(id_funcionario_docente= id_funcionario_docente_encargado).values('id_funcionario_docente'))[0]['id_funcionario_docente']
                id_materia= item.id_cita.id_materia.id_materia
                nro_curso= item.id_cita.nro_curso
                motivo= item.motivo
                hora_inicio= item.id_cita.datetime_inicio_estimado.strftime('%H:%M')
                hora_fin= item.id_cita.datetime_fin_estimado.strftime('%H:%M')
                auxiliar= {'id_facultad': id_facultad, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 'id_materia': id_materia, 'nro_curso': nro_curso, 'motivo': motivo, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Cita de Tutoría'
        context['entity'] = 'Tutoría'
        context['list_url'] = self.success_url
        context['action'] = 'iniciar'
        context['det'] = json.dumps(self.get_details_participantes())
        context['cita'] = json.dumps(self.get_datos_cita())
        return context        


#Clase parta iniciar una cita tipo Orientacion Academica
class CitaOrientacionAcademicaIniciarView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/iniciar_cita_orientacion_academica.html'
    success_url = 'running-event-list/orientacionAcademica/'
    permission_required = 'calendarapp.iniciar_cita'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'iniciar':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='finalizado').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica anterior
                    # ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  - con la logica actual
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    
                    #convertimos nuestras fechas en formato datetime 
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio_real = datetime.strptime(actividad_academica['datetime_inicio_real'], "%Y-%m-%d %H:%M:%S")
                    fecha_hora_fin_real = datetime.strptime(actividad_academica['datetime_fin_real'], "%Y-%m-%d %H:%M:%S")
                    
                    #obtener las instancias de los objectos 
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    
                    if (actividad_academica['id_materia'] != ''):
                        #obtenemos la instancia de la materia
                        ins_materia= Materia.objects.get(id_materia= actividad_academica['id_materia'])
                        cita.id_materia= ins_materia
                        
                    cita.id_estado_actividad_academica = id_estado
                    cita.id_departamento= ins_departamento
                    cita.id_facultad= ins_facultad
                    cita.id_funcionario_docente_encargado= ins_func_doc_encargado
                    cita.datetime_inicio_real= fecha_hora_inicio_real
                    cita.datetime_fin_real = fecha_hora_fin_real
                    cita.nro_curso= actividad_academica['nro_curso']
                    dict = model_to_dict(request.user)
                    cita.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    cita.observacion= actividad_academica['observacion']  
                    cita.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= cita.id_actividad_academica)
                    
                    # #tambien damos de alta el modelo hijo de cita
                    cita_hijo= Cita.objects.get(id_cita= ins_actividad_academica)
                    cita_hijo.motivo= actividad_academica['motivo']
                    cita_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                    
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save() 
                        
                    ori_academ= OrientacionAcademica()
                    #traer ins de cita
                    ins_cita= Cita.objects.get(id_cita= self.get_object().id_actividad_academica)
                    ori_academ.id_orientacion_academica= ins_actividad_academica
                    ori_academ.id_cita= ins_cita
                    ins_tipo_orientacion_academica= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica= actividad_academica['id_tipo_orientacion_academica'])
                    ins_motivo_orientacion_academica= Motivo.objects.get(id_motivo= actividad_academica['id_motivo_ori_academ'])
                    ori_academ.id_tipo_orientacion_academica= ins_tipo_orientacion_academica
                    ori_academ.id_motivo = ins_motivo_orientacion_academica
                    ori_academ.save()      
                    
                    if actividad_academica['tareas']:
                        #obtenemos la persona que esta dando de alta 
                                current_user = request.user
                                dict = model_to_dict(current_user)
                                id_persona=  dict["id_persona"]
                                ins_persona= Persona.objects.get(id= id_persona)
                                for i in actividad_academica['tareas']:
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_orientacion_academica= ori_academ
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada, agregar quien finalizo
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                    
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.observacion=  i['observacion']
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.save()                        
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_datos_cita(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ, incluido el campo de motivo de la tabla cita
            ins_cita = Cita.objects.filter(id_cita= self.get_object().id_actividad_academica).select_related("id_cita")
            for item in ins_cita:
                id_facultad= item.id_cita.id_facultad.id_facultad
                id_funcionario_docente_encargado= item.id_cita.id_funcionario_docente_encargado
                #traemos solo el id del func_doc
                id_funcionario_docente_encargado= list(FuncionarioDocente.objects.filter(id_funcionario_docente= id_funcionario_docente_encargado).values('id_funcionario_docente'))[0]['id_funcionario_docente']
                nro_curso= item.id_cita.nro_curso
                motivo= item.motivo
                hora_inicio= item.id_cita.datetime_inicio_estimado.strftime('%H:%M')
                hora_fin= item.id_cita.datetime_fin_estimado.strftime('%H:%M')
                auxiliar= {'id_facultad': id_facultad, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 'nro_curso': nro_curso, 'motivo': motivo, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Cita de Orientación Académica'
        context['entity'] = 'Orientación Académica'
        context['list_url'] = self.success_url
        context['action'] = 'iniciar'
        context['det'] = json.dumps(self.get_details_participantes())
        context['cita'] = json.dumps(self.get_datos_cita())
        return context        
    
def obtener_horarios_cita(request):
    
    tipo = request.GET.get('tipo_acti_academica')
    func_doc = request.GET.get('id_func_doc')
    parametro= 0
    try:
        #el parametro cargaremos en minuto y ese vamos a tomar como valor para poder calcular el tiempo entre horarios del funcionario/docente
        #/*************************Inicio funcion para generar los horarios****************************************/
        def dividir_horarios_por_minuto(minuto, hora_inicio, hora_fin, dia, id_convocatoria):
            # Convertir los horarios de strings a objetos datetime
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
            hora_fin = datetime.strptime(hora_fin, '%H:%M:%S').time()

            # Calcular la diferencia en minuto entre la hora de inicio y fin
            diferencia = timedelta(hours=hora_fin.hour, minutes=hora_fin.minute) - timedelta(hours=hora_inicio.hour, minutes=hora_inicio.minute)
            minuto_totales = int(diferencia.total_seconds() / 60)

            # Dividir la diferencia en minuto según el parámetro "minuto"
            divisiones = []
            for i in range(minuto, minuto_totales + minuto, minuto):
                hora_inicio_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i-minuto)).time()
                hora_fin_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i)).time()

                if(hora_fin_division <= hora_fin):
                    divisiones.append({"hora_inicio": hora_inicio_division, "hora_fin":hora_fin_division, "dia": dia, "id_convocatoria": id_convocatoria})

            return divisiones

        #/*****************************Fin funcion para generar los horarios****************************************/

        '''El campo de parametro cargaremos en minuto y ese vamos a tomar como valor para poder calcular el tiempo de proceso entre horarios del 
        funcionario/docente primero traemos el parametro de minuto que se encuentra disponible de acuerdo a la actividad academica (tuto u orie academ ) '''

        if tipo== "tutoria":
            parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minuto').values('valor')
            parametro= parametro[0]['valor']
            
        elif tipo== "ori_academica":
            parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minuto').values('valor')
            parametro= parametro[0]['valor']
        else:
            parametro= 0

        #vamos a consultar los horarios cargados del funcionario_docente solicitado cuyo semestre aun no haya finalizado    
        horario_func_doc= HorarioSemestral.objects.filter(id_funcionario_docente= func_doc, id_convocatoria__fecha_fin__gt = datetime.now())
        # Convertir el queryset a JSON en formato de cadena (str)
        horario_func_doc= serializers.serialize('json', horario_func_doc)
        
        # Convertir la cadena JSON a un diccionario
        horario_func_doc = json.loads(horario_func_doc)
        
        #print(horario_func_doc)

        
        #generamos varias listas para agregar las fechas y horas de acuerdo al dia de la semana 
        fechas_lunes = []  # Lista para almacenar las fechas de lunes
        fechas_martes = []  # Lista para almacenar las fechas de martes
        fechas_miercoles = []  # Lista para almacenar las fechas de miercoles
        fechas_jueves = []  # Lista para almacenar las fechas de jueves
        fechas_viernes = []  # Lista para almacenar las fechas de viernes
        fechas_sabado = []  # Lista para almacenar las fechas de sabados

        calendario_semestral = [] #lista intermedia para guardar los horarios del func/doc con los campos interesados que seran iterados
        horarios= [] #lista para ir guardando todos los horarios cargados del fun/doc en la base de datos
        horas_dia= [] #lista auxiliar para ir iterando los registros de horarios generados para el func/doc por registro

        horarios_disponibles= pd.DataFrame() #lista final para devolver el resultado del metodo
        fecha_hoy= datetime.now()
        auxiliar= []

        #iteramos cada registro del calendario funcionario/docente consultado de la bd y por cada item vamos generando las fechas con los horarios
        if horario_func_doc: #validamos si la consulta devolvio registros para iniciar la iteración
            for item in horario_func_doc:
                hora_inicio = item['fields']['hora_inicio']
                hora_fin = item['fields']['hora_fin']
                id_convocatoria = item['fields']['id_convocatoria']
                id_dia = item['fields']['id_dia']
                
                calendario_semestral.append({"id_dia": id_dia, "id_convocatoria": id_convocatoria , "hora_inicio": hora_inicio, "hora_fin": hora_fin})


        #volvemos a iterar los elementos de la lista construida con los valores seleccionados
        if calendario_semestral: #validamos que tenga datos
            for item in calendario_semestral:
                auxiliar= []
                id_dia= item["id_dia"]
                id_convocatoria= item["id_convocatoria"]
                hora_inicio = item['hora_inicio']
                hora_fin = item['hora_fin']

                #tengo que buscar todas las fechas que se generan de acuerdo al dia que cae para el horario, hasta el ultimo dia del semestre
                #generamos los parametros que utilizaremos par extraer las fechas y horarios 
                #traer el dia 
                dia= Dia.objects.filter(id_dia= id_dia).values('descripcion_dia').first()
                dia= dia['descripcion_dia']
                #traer la ultima fecha del semestre actual
                fin_semestre= Convocatoria.objects.filter(id_convocatoria= id_convocatoria).values('fecha_fin').first()
                
                fecha_inicial = fecha_hoy.date()  # Fecha inicial, dia de hoy para generar las citas, inclusive
                fecha_fin = fin_semestre["fecha_fin"]  # Fecha de finalización, inclusive

                #generar todas las fechas por dia de semana para todo el semestre
                while fecha_inicial <= fecha_fin:
                    if (fecha_inicial.weekday() == 0 and dia == 'Lunes'):  # 0 corresponde al día lunes
                        fechas_lunes.append({"fecha": fecha_inicial, "dia": 'Lunes' })
                    elif (fecha_inicial.weekday() == 1 and dia == 'Martes'):
                        fechas_martes.append({"fecha": fecha_inicial, "dia": 'Martes' })
                    elif (fecha_inicial.weekday() == 2 and dia == 'Miércoles'):
                        fechas_miercoles.append({"fecha": fecha_inicial, "dia": 'Miércoles' })
                    elif (fecha_inicial.weekday() == 3 and dia == 'Jueves'):
                        fechas_jueves.append({"fecha": fecha_inicial, "dia": 'Jueves' })
                    elif (fecha_inicial.weekday() == 4 and dia == 'Viernes'):
                        fechas_viernes.append({"fecha": fecha_inicial, "dia": 'Viernes' })
                    elif (fecha_inicial.weekday() == 5 and dia == 'Sábado'):
                        fechas_sabado.append({"fecha": fecha_inicial, "dia": 'Sábado' })
                    
                    fecha_inicial += timedelta(days=1)


                '''una vez generado todas las fechas de acuerdo al dia correspondiente vamos a crear otro listado con las horas, dias y 
                convocatoria que corresponde'''
                auxiliar= dividir_horarios_por_minuto(parametro, hora_inicio, hora_fin, dia, id_convocatoria) #esto me genera un objeto de tipo lista que posee elementos de tipo lista que a su vez guarda diccionarios
                horas_dia.append(auxiliar)
                
                #recorremos todos los horarios y por cada horario vamos iterando nuevamente las fechas y agregando en la lista final de horarios
                for dato in horas_dia:
                    for item in dato:
                        hora_inicio = item['hora_inicio']
                        hora_fin = item['hora_fin']
                        convocatoria= item['id_convocatoria']
                        
                        #recorremos la lista de acuerdo al dia y vamos generando los horarios
                        if dia == 'Lunes': #preguntamos si el dia el lunes entonces iteramos en los horarios de los lunes 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_lunes:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
                        
                        elif dia == 'Martes': #preguntamos si el dia el martes entonces iteramos en los horarios de los martes 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_martes:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
                        
                        elif dia == 'Miércoles': #preguntamos si el dia el miercoles entonces iteramos en los horarios de los miercoles 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_miercoles:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})
                        
                        elif dia == 'Jueves': #preguntamos si el dia el jueves entonces iteramos en los horarios de los jueves 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_jueves:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

                        
                        elif dia == 'Viernes': #preguntamos si el dia el viernes entonces iteramos en los horarios de los viernes 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_viernes:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

                        elif dia == 'Sábado': #preguntamos si el dia el sabado entonces iteramos en los horarios de los sabados 
                            #iteramos la lista y a medida que vamos iterando le vamos agregando las horas
                            for dt in fechas_sabado:
                                fecha= dt['fecha']
                                dia= dt['dia']
                                horarios.append({"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin, "dia": dia, "convocatoria": convocatoria})

                horas_dia= [] #vaciamos para el siguiente registro del calendario
            
        #en caso que no tenga ningun calendario el func/doc vamos a crear uno vacio
        if horarios:
            df2 = pd.DataFrame(horarios)
        else:
            df2 = pd.DataFrame()
            
        #print(df2,'horarios del calendario')
        
        #df2.to_excel("C:/Users/beatr/Documents/df2.xlsx", index=False)

        '''ahora que ya tenemos generado todos los horarios por dias vamos a preguntar cuales de ellos ya estan con estado "Pendiente" para poder excluir
        traer todos los registros de citas donde la convocatoria aun no haya terminado y la fecha sea de hoy con la hora superior a la actual '''

        if tipo== "tutoria":
            actividades_academicas= Cita.objects.filter(Q(id_cita__datetime_inicio_estimado__gt=fecha_hoy) | Q(id_cita__datetime_inicio_real__gt=fecha_hoy), es_tutoria=True, id_cita__id_funcionario_docente_encargado= func_doc, id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica__contains='pendiente').values('id_cita__datetime_inicio_estimado')
            
        elif tipo== "ori_academica":
            actividades_academicas= Cita.objects.filter(Q(id_cita__datetime_inicio_estimado__gt=fecha_hoy) | Q(id_cita__datetime_inicio_real__gt=fecha_hoy), es_orientacion_academica=True, id_cita__id_funcionario_docente_encargado= func_doc, id_cita__id_estado_actividad_academica__descripcion_estado_actividad_academica__contains='pendiente').values('id_cita__datetime_inicio_estimado')

        else:
            actividades_academicas= Cita.objects.none()
        
        #print(actividades_academicas,'actividades academicas')

        #creamos una lista auxiliar para ir pasando ahi los items 
        lista_provisoria= []

        if actividades_academicas.exists(): #preguntamos si posee datos 
            #print('entro')
            for item in actividades_academicas:
                    fecha= item['id_cita__datetime_inicio_estimado']            
                    lista_provisoria.append({'fecha': fecha,'hora_inicio': fecha})
                
            dt_aa= pd.DataFrame(lista_provisoria)
            dt_aa['fecha'] = pd.to_datetime(dt_aa['fecha']).dt.date
            dt_aa['hora_inicio'] = pd.to_datetime(dt_aa['hora_inicio']).dt.time
            
        else: #si no devolvio ningun registro la consulta creamos un dt vacio
            dt_aa= pd.DataFrame()
        
        
        # Mapear el número de mes al nombre en español
        meses_espanol = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
            
        '''caso si tiene registros de calendario y hay casos para excluir se procede a hacer la exclusion
        preguntamos si es que ambos dt estan con datos entonces hacemos la exclusion'''
        if (not dt_aa.empty and not df2.empty):
            print('entro en exclusion')
            # Convertir en tipos de datos correctos para poder operar
            df2['fecha'] = pd.to_datetime(df2['fecha']).dt.date
            df2['dia'] = df2['dia'].astype(str)
            df2['hora_inicio'] = pd.to_datetime(df2["hora_inicio"].astype(str)).dt.time
            df2['hora_fin'] = pd.to_datetime(df2["hora_fin"].astype(str)).dt.time

            #ordenamos por fecha 
            df2.sort_values(by='fecha', inplace=True)

            #procedemos a borrar duplicados
            df2.drop_duplicates(keep='first', inplace=True)

            # Eliminar registros donde fecha sea hoy y la hora_inicio supere la hora actual
            df2.drop(df2[(df2['fecha'] == datetime.now().date()) & (df2['hora_inicio'] < datetime.now().time())].index, inplace=True)
            
            #excluir los horarios que ya se encuentren reservados 
            ''' agregamos una columna llamada '_merge' con la etiqueta del origen de cada registro ('both', 'left_only' o 'right_only') 
            utilizando el parámetro indicator=True. Merge de los dataframes con indicator=True
            Finalmente, filtramos los registros que solo están presentes en el primer dataframe (etiqueta 'left_only') y eliminamos la 
            columna '_merge' para obtener el resultado deseado en el dataframe df_filtered.'''
        
            merged_df = df2.merge(dt_aa, on=['fecha', 'hora_inicio'], how='left', indicator=True)
            df_filtered = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
            #agregar columna de Mes
            df_filtered['mes'] = df_filtered['fecha'].apply(lambda x: meses_espanol[x.month])
            # Formatear la columna 'fecha' con el formato 'dd-mm-yyyy'
            df_filtered['fecha'] = df_filtered['fecha'].apply(lambda x: x.strftime('%d-%m-%Y'))
            horarios_disponibles= df_filtered

        # caso si no exite otras citas y tiene calendario devolver los horarios sin exclusion
        elif (not df2.empty and dt_aa.empty):
            print('entro en no exclusion')
            # Convertir en tipos de datos correctos para poder operar
            df2['fecha'] = pd.to_datetime(df2['fecha']).dt.date
            df2['dia'] = df2['dia'].astype(str)
            df2['hora_inicio'] = pd.to_datetime(df2["hora_inicio"].astype(str)).dt.time
            df2['hora_fin'] = pd.to_datetime(df2["hora_fin"].astype(str)).dt.time
            
            # Eliminar registros donde fecha sea hoy y la hora_inicio supere la hora actual
            df2.drop(df2[(df2['fecha'] == datetime.now().date()) & (df2['hora_inicio'] < datetime.now().time())].index, inplace=True)
            
             #ordenamos por fecha 
            df2.sort_values(by='fecha', inplace=True)
            
            #agregar columna de Mes
            df2['mes'] = df2['fecha'].apply(lambda x: meses_espanol[x.month])
            
            # Formatear la columna 'fecha' con el formato 'dd-mm-yyyy'
            df2['fecha'] = df2['fecha'].apply(lambda x: x.strftime('%d-%m-%Y'))
            
            horarios_disponibles= df2
            
        # caso si el fun/doc no tiene ningun calendario disponible devolver resultado vacio
        elif (df2.empty):
            horarios_disponibles= pd.DataFrame()
            
        
            
        #Finalmente devolvemos un JSON 
        horarios_disponibles.to_excel("C:/Users/beatr/Documents/horarios_disponibles.xlsx", index=False)

        '''El método to_json() también admite otros formatos de orientación, como 'split', 'index', 'columns', 'values' y 'table', para adaptarse 
        a diferentes necesidades de estructura JSON. Puedes revisar la documentación de pandas para obtener más detalles sobre estos formatos.'''
        horarios_disponibles= horarios_disponibles.to_json(orient='records')
        
        # print(type(horarios_disponibles))
        # print(horarios_disponibles)
    except Exception as e:
            print(f"Se ha producido un error: {e}")

    return JsonResponse(horarios_disponibles, safe=False)


#clase de creacion para una actividad academica de tipo tutoria
class TutoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin ,CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/tutoria_create.html'
    success_url = 'running-acti_academ-list/Tutoria/' #reverse_lazy('calendarapp:calenders')
    permission_required = 'calendarapp.registrar_actividad_academica'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'add':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    tutoria = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='iniciada').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    ins_solicitante= Persona.objects.get(id= actividad_academica['id_solicitante'])
                    
                    tutoria.id_estado_actividad_academica = id_estado
                    tutoria.id_departamento= ins_departamento
                    tutoria.id_convocatoria = ins_convocatoria
                    tutoria.id_facultad= ins_facultad
                    tutoria.id_materia= ins_materia
                    tutoria.id_funcionario_docente_encargado= ins_func_doc_encargado
                    tutoria.id_persona_alta= ins_persona
                    tutoria.id_persona_ultima_modificacion= ins_persona
                    tutoria.id_persona_solicitante= ins_solicitante
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    tutoria.datetime_inicio_real= datetime.now()
                    #tutoria.datetime_fin_real= fecha_hora_fin
                    tutoria.nro_curso= actividad_academica['nro_curso']
                    tutoria.observacion= actividad_academica['observacion']
                    tutoria.datetime_registro= datetime.now()
                    tutoria.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= tutoria.id_actividad_academica)
                    
                    # #tambien damos de alta el hijo de Event (tutoria)
                    tutoria_hijo= Tutoria()
                    tutoria_hijo.id_tutoria= ins_actividad_academica
                    ins_tipo_tutoria=  TipoTutoria.objects.get(id_tipo_tutoria= actividad_academica['id_tipo_tutoria'])
                    tutoria_hijo.id_tipo_tutoria= ins_tipo_tutoria
                    tutoria_hijo.nombre_trabajo= actividad_academica['nombre_trabajo'] 
                    tutoria_hijo.save()
                    
                    #guardamos el detalle de participantes
                    if actividad_academica['participantes']:
                            for i in actividad_academica['participantes']:
                                det_acti = DetalleActividadAcademica()
                                det_acti.id_actividad_academica= ins_actividad_academica
                                #obtenemos el id persona del participante
                                ins_participante= Persona.objects.get(id= i['id'])
                                det_acti.id_participante= ins_participante
                                det_acti.save()
                                
                    #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                tarea = Tarea()
                                tarea.id_persona_alta= ins_persona
                                tarea.id_tutoria= tutoria_hijo
                                ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                tarea.id_estado_tarea= ins_estado_tarea
                                ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                tarea.id_tipo_tarea= ins_tipo_tarea
                                ins_responsable= Persona.objects.get(id= i['responsable'])
                                #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.id_persona_finalizacion= ins_responsable
                                    
                                #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                
                                tarea.id_persona_responsable= ins_responsable
                                tarea.datetime_alta= datetime.now()
                                tarea.id_persona_ultima_modificacion= ins_persona
                                tarea.observacion=  i['observacion']
                                tarea.save()
                                
            #para finalizar la tutoria
            elif action == 'addfinalizar':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    tutoria = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='finalizado').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    ins_solicitante= Persona.objects.get(id= actividad_academica['id_solicitante'])
                    
                    tutoria.id_estado_actividad_academica = id_estado
                    tutoria.id_departamento= ins_departamento
                    tutoria.id_convocatoria = ins_convocatoria
                    tutoria.id_facultad= ins_facultad
                    tutoria.id_materia= ins_materia
                    tutoria.id_funcionario_docente_encargado= ins_func_doc_encargado
                    tutoria.id_persona_alta= ins_persona
                    tutoria.id_persona_ultima_modificacion= ins_persona
                    tutoria.id_persona_solicitante= ins_solicitante
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    tutoria.datetime_inicio_real= fecha_hora_inicio
                    tutoria.datetime_fin_real= datetime.now()
                    tutoria.nro_curso= actividad_academica['nro_curso']
                    tutoria.observacion= actividad_academica['observacion']
                    tutoria.datetime_registro= datetime.now()
                    tutoria.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= tutoria.id_actividad_academica)
                    
                    # #tambien damos de alta el hijo de Event (tutoria)
                    tutoria_hijo= Tutoria()
                    tutoria_hijo.id_tutoria= ins_actividad_academica
                    ins_tipo_tutoria=  TipoTutoria.objects.get(id_tipo_tutoria= actividad_academica['id_tipo_tutoria'])
                    tutoria_hijo.id_tipo_tutoria= ins_tipo_tutoria
                    tutoria_hijo.nombre_trabajo= actividad_academica['nombre_trabajo'] 
                    tutoria_hijo.save()
                    
                    #guardamos el detalle de participantes
                    if actividad_academica['participantes']:
                            for i in actividad_academica['participantes']:
                                det_acti = DetalleActividadAcademica()
                                det_acti.id_actividad_academica= ins_actividad_academica
                                #obtenemos el id persona del participante
                                ins_participante= Persona.objects.get(id= i['id'])
                                det_acti.id_participante= ins_participante
                                det_acti.save()
                                
                    #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                tarea = Tarea()
                                tarea.id_persona_alta= ins_persona
                                tarea.id_tutoria= tutoria_hijo
                                ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                tarea.id_estado_tarea= ins_estado_tarea
                                ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                tarea.id_tipo_tarea= ins_tipo_tarea
                                ins_responsable= Persona.objects.get(id= i['responsable'])
                                #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada, agregar quien finalizo
                                if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.id_persona_finalizacion= ins_responsable
                                
                                #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                
                                tarea.id_persona_responsable= ins_responsable
                                tarea.datetime_alta= datetime.now()
                                tarea.id_persona_ultima_modificacion= ins_persona
                                tarea.observacion=  i['observacion']
                                tarea.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            #probar
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de una Tutoría'
        context['entity'] = 'Tutoría'
        context['list_url'] = self.success_url
        return context
    
    
#clase de creacion para una actividad academica de tipo orientacion academica
class OrientacionAcademicaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin ,CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/orientacion_academica_create.html'
    success_url = 'running-acti_academ-list/OriAcademica/' #reverse_lazy('calendarapp:calenders')
    permission_required = 'calendarapp.registrar_actividad_academica'
    #url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'add':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    orientacion_academica = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='iniciada').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica anterior
                    #ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  -- logica actual
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
        
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    ins_solicitante= Persona.objects.get(id= actividad_academica['id_solicitante'])
                    
                    orientacion_academica.id_estado_actividad_academica = id_estado
                    orientacion_academica.id_departamento= ins_departamento
                    orientacion_academica.id_convocatoria = ins_convocatoria
                    orientacion_academica.id_facultad= ins_facultad
                    orientacion_academica.id_funcionario_docente_encargado= ins_func_doc_encargado
                    orientacion_academica.id_persona_alta= ins_persona
                    orientacion_academica.id_persona_solicitante= ins_persona
                    orientacion_academica.id_persona_ultima_modificacion= ins_persona
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    orientacion_academica.datetime_inicio_real= datetime.now()
                    #orientacion_academica.datetime_fin_real= datetime.now()
                    orientacion_academica.nro_curso= actividad_academica['nro_curso']
                    orientacion_academica.datetime_registro= datetime.now()
                    orientacion_academica.id_persona_solicitante= ins_solicitante
                    orientacion_academica.observacion= actividad_academica['observacion']
                    orientacion_academica.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= orientacion_academica.id_actividad_academica)
                    
                   #tambien damos de alta el hijo de Event (orientacion academica)
                    ori_academ_hijo= OrientacionAcademica()
                    ori_academ_hijo.id_orientacion_academica= ins_actividad_academica
                    ins_tipo_orientacion_academica= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica= actividad_academica['id_tipo_orientacion_academica'])
                    ins_motivo_orientacion_academica= Motivo.objects.get(id_motivo= actividad_academica['id_motivo_ori_academ'])
                    ori_academ_hijo.id_tipo_orientacion_academica= ins_tipo_orientacion_academica
                    ori_academ_hijo.id_motivo = ins_motivo_orientacion_academica
                    ori_academ_hijo.save()
                    
                    #guardamos el detalle de participantes
                    if actividad_academica['participantes']:
                            for i in actividad_academica['participantes']:
                                det_acti = DetalleActividadAcademica()
                                det_acti.id_actividad_academica= ins_actividad_academica
                                #obtenemos el id persona del participante
                                ins_participante= Persona.objects.get(id= i['id'])
                                det_acti.id_participante= ins_participante
                                det_acti.save()
                                
                    #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                tarea = Tarea()
                                tarea.id_persona_alta= ins_persona
                                tarea.id_orientacion_academica= ori_academ_hijo
                                ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                tarea.id_estado_tarea= ins_estado_tarea
                                ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                tarea.id_tipo_tarea= ins_tipo_tarea
                                ins_responsable= Persona.objects.get(id= i['responsable'])
                                #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.id_persona_finalizacion= ins_responsable
                                    
                                #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                
                                tarea.id_persona_responsable= ins_responsable
                                tarea.datetime_alta= datetime.now()
                                tarea.id_persona_ultima_modificacion= ins_persona
                                tarea.observacion=  i['observacion']
                                tarea.save()
                                
            #para finalizar la orientacion academica
            elif action == 'addfinalizar':
                #realizamos todo al mismo tiempo
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    orientacion_academica = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='finalizado').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica anterior
                    #ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  -- logica actual
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
        
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    ins_persona= Persona.objects.get(id= id_persona)
                    ins_solicitante= Persona.objects.get(id= actividad_academica['id_solicitante'])
                    
                    #consultamos si la materia existe
                    if actividad_academica['id_materia'] != '' or actividad_academica['id_materia'] != '.':
                        ins_materia= Materia.objects.get(id_materia= actividad_academica['id_materia'])
                        orientacion_academica.id_materia= ins_materia    
                    orientacion_academica.id_estado_actividad_academica = id_estado
                    orientacion_academica.id_departamento= ins_departamento
                    orientacion_academica.id_convocatoria = ins_convocatoria
                    orientacion_academica.id_facultad= ins_facultad
                    orientacion_academica.id_funcionario_docente_encargado= ins_func_doc_encargado
                    orientacion_academica.id_persona_alta= ins_persona
                    orientacion_academica.id_persona_solicitante= ins_persona
                    orientacion_academica.id_persona_ultima_modificacion= ins_persona
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    orientacion_academica.datetime_inicio_real= fecha_hora_inicio
                    orientacion_academica.datetime_fin_real= datetime.now()
                    orientacion_academica.nro_curso= actividad_academica['nro_curso']
                    orientacion_academica.datetime_registro= datetime.now()
                    orientacion_academica.id_persona_solicitante= ins_solicitante
                    orientacion_academica.observacion= actividad_academica['observacion']
                    orientacion_academica.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= orientacion_academica.id_actividad_academica)
                    
                   #tambien damos de alta el hijo de Event (orientacion academica)
                    ori_academ_hijo= OrientacionAcademica()
                    ori_academ_hijo.id_orientacion_academica= ins_actividad_academica
                    ins_tipo_orientacion_academica= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica= actividad_academica['id_tipo_orientacion_academica'])
                    ins_motivo_orientacion_academica= Motivo.objects.get(id_motivo= actividad_academica['id_motivo_ori_academ'])
                    ori_academ_hijo.id_tipo_orientacion_academica= ins_tipo_orientacion_academica
                    ori_academ_hijo.id_motivo = ins_motivo_orientacion_academica
                    ori_academ_hijo.save()
                    
                    #guardamos el detalle de participantes
                    if actividad_academica['participantes']:
                            for i in actividad_academica['participantes']:
                                det_acti = DetalleActividadAcademica()
                                det_acti.id_actividad_academica= ins_actividad_academica
                                #obtenemos el id persona del participante
                                ins_participante= Persona.objects.get(id= i['id'])
                                det_acti.id_participante= ins_participante
                                det_acti.save()
                                
                    #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                tarea = Tarea()
                                tarea.id_persona_alta= ins_persona
                                tarea.id_orientacion_academica= ori_academ_hijo
                                ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                tarea.id_estado_tarea= ins_estado_tarea
                                ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                tarea.id_tipo_tarea= ins_tipo_tarea
                                ins_responsable= Persona.objects.get(id= i['responsable'])
                                #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    tarea.id_persona_finalizacion= ins_responsable
                                    
                                #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                    tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                    tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                
                                tarea.id_persona_responsable= ins_responsable
                                tarea.datetime_alta= datetime.now()
                                tarea.id_persona_ultima_modificacion= ins_persona
                                tarea.observacion=  i['observacion']
                                tarea.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            #probar
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de una Orientación Académica'
        context['entity'] = 'Orientación Académica'
        context['list_url'] = self.success_url
        return context
    
    
#Clase de editar de una actividad academica tipo Tutoria
class TutoriaUpdateView(LoginRequiredMixin,  ValidatePermissionRequiredMixin ,UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/tutoria_edit.html'
    success_url = 'running-acti_academ-list/Tutoria/'
    permission_required = 'calendarapp.editar_actividad_academica'
    #url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    tutoria = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    #id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Iniciada').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    
                    
                    #el estado se mantiene igual
                    #tutoria.id_estado_actividad_academica = id_estado
                    tutoria.id_departamento= ins_departamento
                    tutoria.id_convocatoria = ins_convocatoria
                    tutoria.id_facultad= ins_facultad
                    tutoria.id_materia= ins_materia
                    tutoria.id_funcionario_docente_encargado= ins_func_doc_encargado
                    #la persona se mantiene
                    #tutoria.id_persona_alta= ins_persona
                    dict = model_to_dict(request.user)
                    tutoria.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    tutoria.nro_curso= actividad_academica['nro_curso']
                    tutoria.observacion= actividad_academica['observacion']
                    tutoria.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= tutoria.id_actividad_academica)
                    
                    #tambien modificamos el modelo hijo de tutoria
                    tutoria_hijo = Tutoria.objects.get(id_tutoria = self.get_object().id_actividad_academica)
                    ins_tipo_tutoria=  TipoTutoria.objects.get(id_tipo_tutoria= actividad_academica['id_tipo_tutoria'])
                    tutoria_hijo.id_tipo_tutoria= ins_tipo_tutoria
                    tutoria_hijo.nombre_trabajo= actividad_academica['nombre_trabajo'] 
                    tutoria_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                        
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    ins_persona= Persona.objects.get(id= id_persona)                    
                    
                   #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                #por cada elemento consultamos el valor del id para comprobar si se trata de una tarea nueva o de una actualizacion de registro
                                
                                #se trata de un nuevo registro
                                if i['id'] == "":
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_tutoria= tutoria_hijo
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                        
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.observacion=  i['observacion']
                                    tarea.save()
                                    
                                else: #se trata de un registro ya existente
                                    #obtenemos el registro de la tarea para poder actualizar
                                    item_actual= Tarea.objects.filter(id_tarea= i['id']).first()
                                    #pisamos los campos
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    item_actual.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    item_actual.id_tipo_tarea= ins_tipo_tarea
                                    
                                    #si la tarea ya esta finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        if item_actual.datetime_inicio_real is None:
                                            item_actual.datetime_inicio_real= datetime.now()
                                        item_actual.datetime_finalizacion= datetime.now()
                                        item_actual.id_persona_finalizacion= ins_persona
                                        
                                    #si la tarea esta iniciada
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        item_actual.datetime_inicio_real= datetime.now()      
                                            
                                    item_actual.id_persona_ultima_modificacion= ins_persona
                                    item_actual.observacion=  i['observacion']
                                    item_actual.save()     
            
            elif action == 'editfinalizar':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    tutoria = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizado').first()
                    #buscamos el departamento al cual esta asociado la materia
                    id_materia= actividad_academica['id_materia']
                    id_departamento= Materia.objects.filter(id_materia= id_materia).values("id_departamento").first()
                    id_departamento= id_departamento["id_departamento"]
                    ins_departamento= Departamento.objects.get(id_departamento= id_departamento)
                    
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_materia= Materia.objects.get(id_materia= id_materia)
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])

                    #el estado se mantiene igual
                    tutoria.id_estado_actividad_academica = id_estado
                    tutoria.id_departamento= ins_departamento
                    tutoria.id_convocatoria = ins_convocatoria
                    tutoria.id_facultad= ins_facultad
                    tutoria.id_materia= ins_materia
                    tutoria.id_funcionario_docente_encargado= ins_func_doc_encargado
                    #la persona se mantiene
                    #tutoria.id_persona_alta= ins_persona
                    dict = model_to_dict(request.user)
                    tutoria.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    tutoria.datetime_fin_real= datetime.now()
                    tutoria.nro_curso= actividad_academica['nro_curso']
                    tutoria.observacion= actividad_academica['observacion']
                    tutoria.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= tutoria.id_actividad_academica)
                    
                    #tambien modificamos el modelo hijo de tutoria
                    tutoria_hijo = Tutoria.objects.get(id_tutoria = self.get_object().id_actividad_academica)
                    ins_tipo_tutoria=  TipoTutoria.objects.get(id_tipo_tutoria= actividad_academica['id_tipo_tutoria'])
                    tutoria_hijo.id_tipo_tutoria= ins_tipo_tutoria
                    tutoria_hijo.nombre_trabajo= actividad_academica['nombre_trabajo'] 
                    tutoria_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    ins_persona= Persona.objects.get(id= id_persona)                    
                    
                   #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                #por cada elemento consultamos el valor del id para comprobar si se trata de una tarea nueva o de una actualizacion de registro
                                
                                #se trata de un nuevo registro
                                if i['id'] == "":
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_tutoria= tutoria_hijo
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                        
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.observacion=  i['observacion']
                                    tarea.save()
                                    
                                else: #se trata de un registro ya existente
                                    #obtenemos el registro de la tarea para poder actualizar
                                    item_actual= Tarea.objects.filter(id_tarea= i['id']).first()
                                    #pisamos los campos
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    item_actual.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    item_actual.id_tipo_tarea= ins_tipo_tarea
                                    
                                    #si la tarea ya esta finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        if item_actual.datetime_inicio_real is None:
                                            item_actual.datetime_inicio_real= datetime.now()
                                        item_actual.datetime_finalizacion= datetime.now()
                                        item_actual.id_persona_finalizacion= ins_persona
                                        
                                    #si la tarea esta iniciada
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        item_actual.datetime_inicio_real= datetime.now()      
                                            
                                    item_actual.id_persona_ultima_modificacion= ins_persona
                                    item_actual.observacion=  i['observacion']
                                    item_actual.save()                     
                
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_datos_event(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            ins_evet = Event.objects.get(id_actividad_academica= self.get_object().id_actividad_academica)
            id_estado_actividad_academica= ins_evet.id_estado_actividad_academica.id_estado_actividad_academica
            id_convocatoria= ins_evet.id_convocatoria.id_convocatoria
            id_facultad= ins_evet.id_facultad.id_facultad
            if ins_evet.id_materia:
                id_materia= ins_evet.id_materia.id_materia
            else:
                id_materia= ''
            id_departamento= ins_evet.id_departamento.id_departamento
            id_funcionario_docente_encargado= ins_evet.id_funcionario_docente_encargado.id_funcionario_docente.id
            if ins_evet.id_persona_solicitante:
                id_persona_solicitante= ins_evet.id_persona_solicitante.id
            else:
                id_persona_solicitante= ''
            id_persona_alta= ins_evet.id_persona_alta.id
            datetime_inicio_estimado= ins_evet.datetime_inicio_estimado.strftime('%d-%m-%Y %H:%M:%S')
            datetime_fin_estimado = ins_evet.datetime_fin_estimado.strftime('%d-%m-%Y %H:%M:%S')
            if ins_evet.datetime_inicio_real:
                datetime_inicio_real = ins_evet.datetime_inicio_real.strftime('%d-%m-%Y %H:%M:%S')
            else:
                datetime_inicio_real = ''
            if ins_evet.datetime_fin_real:
                datetime_fin_real = ins_evet.datetime_fin_real.strftime('%d-%m-%Y %H:%M:%S')
            else:
                datetime_fin_real = ''
            datetime_registro = ins_evet.datetime_registro.strftime('%d-%m-%Y %H:%M:%S')
            if ins_evet.observacion is None:
                observacion= ''
            else:
                observacion= ins_evet.observacion
            if ins_evet.nro_curso is None: 
                nro_curso= ''
            else:
                nro_curso= ins_evet.nro_curso
            auxiliar= {'id_estado_actividad_academica': id_estado_actividad_academica, 'id_convocatoria': id_convocatoria, 
            'id_facultad': id_facultad, 'id_materia': id_materia, 'id_departamento': id_departamento, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 
            'id_persona_solicitante': id_persona_solicitante, 'id_persona_alta': id_persona_alta, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_fin_estimado': datetime_fin_estimado,
            'datetime_fin_estimado':datetime_fin_estimado, 'datetime_inicio_real': datetime_inicio_real, 'datetime_fin_real': datetime_fin_real, 'datetime_registro': datetime_registro, 'observacion': observacion, 'nro_curso': nro_curso}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_datos_tutoria(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            ins_tutoria = Tutoria.objects.filter(id_tutoria= self.get_object().id_actividad_academica).first()
            id_tipo_tutoria = ins_tutoria.id_tipo_tutoria.id_tipo_tutoria
            nombre_trabajo = ins_tutoria.nombre_trabajo
            auxiliar= {'id_tipo_tutoria': id_tipo_tutoria, 'nombre_trabajo': nombre_trabajo}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_datos_tareas(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            tareas = Tarea.objects.filter(id_tutoria= self.get_object().id_actividad_academica)
            tareas_lista = list(tareas)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_tutoria = tarea.id_tutoria.id_tutoria.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_tutoria': id_tutoria, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}                    
                    data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Tutoría'
        context['entity'] = 'Tutoría'
        context['list_url'] = self.success_url
        context['det'] = json.dumps(self.get_details_participantes())
        context['tutoria'] = json.dumps(self.get_datos_tutoria())
        context['event'] = self.get_datos_event()
        context['tarea'] = self.get_datos_tareas()
        return context
    

#Clase de editar de una actividad academica tipo Orientación Académica
class OrientacionAcademicaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin ,UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/orientacion_academica_edit.html'
    success_url = 'running-acti_academ-list/OriAcademica/'
    permission_required = 'calendarapp.editar_actividad_academica'
    #url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_participantes':
                data = []
                participantes = Persona.objects.filter(documento__icontains=request.POST['term'])[0:10]
                for i in participantes:
                    item = i.toJSON()
                    item['value'] = i.nombre + ' ' + i.apellido
                    data.append(item)
            elif action == 'edit':
                actividad_academica = json.loads(request.POST['actividad_academica'])
                print(type(actividad_academica['id_materia']), ' materia')
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    orientacion_academica = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    #id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Iniciado').first()
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica anterior
                    #ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  -- logica actual
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    
                    #el estado se mantiene igual
                    #orientacion_academica.id_estado_actividad_academica = id_estado
                    #consultamos si la materia existe
                    ins_materia= None
                    if (actividad_academica['id_materia'] != ''):
                        ins_materia= Materia.objects.get(id_materia= actividad_academica['id_materia'])
                        orientacion_academica.id_materia= ins_materia 
                    orientacion_academica.id_departamento= ins_departamento
                    orientacion_academica.id_convocatoria = ins_convocatoria
                    orientacion_academica.id_facultad= ins_facultad
                    orientacion_academica.id_materia= ins_materia
                    orientacion_academica.id_funcionario_docente_encargado= ins_func_doc_encargado
                    #la persona se mantiene
                    #tutoria.id_persona_alta= ins_persona
                    dict = model_to_dict(request.user)
                    orientacion_academica.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    orientacion_academica.nro_curso= actividad_academica['nro_curso']
                    orientacion_academica.observacion= actividad_academica['observacion']
                    orientacion_academica.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= orientacion_academica.id_actividad_academica)
                    
                    #tambien modificamos el modelo hijo de ori academica
                    ori_academ_hijo = OrientacionAcademica.objects.get(id_orientacion_academica = self.get_object().id_actividad_academica)
                    ins_tipo_orientacion_academica= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica= actividad_academica['id_tipo_orientacion_academica'])
                    ins_motivo_orientacion_academica= Motivo.objects.get(id_motivo= actividad_academica['id_motivo_ori_academ'])
                    ori_academ_hijo.id_tipo_orientacion_academica= ins_tipo_orientacion_academica
                    ori_academ_hijo.id_motivo = ins_motivo_orientacion_academica
                    ori_academ_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    ins_persona= Persona.objects.get(id= id_persona)                    
                    
                   #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                #por cada elemento consultamos el valor del id para comprobar si se trata de una tarea nueva o de una actualizacion de registro
                                
                                #se trata de un nuevo registro
                                if i['id'] == "":
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_orientacion_academica= ori_academ_hijo
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                        
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.observacion=  i['observacion']
                                    tarea.save()
                                    
                                else: #se trata de un registro ya existente
                                    #obtenemos el registro de la tarea para poder actualizar
                                    item_actual= Tarea.objects.filter(id_tarea= i['id']).first()
                                    #pisamos los campos
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    item_actual.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    item_actual.id_tipo_tarea= ins_tipo_tarea
                                    
                                    #si la tarea ya esta finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        if item_actual.datetime_inicio_real is None:
                                            item_actual.datetime_inicio_real= datetime.now()
                                        item_actual.datetime_finalizacion= datetime.now()
                                        item_actual.id_persona_finalizacion= ins_persona
                                        
                                    #si la tarea esta iniciada
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        item_actual.datetime_inicio_real= datetime.now()      
                                            
                                    item_actual.id_persona_ultima_modificacion= ins_persona
                                    item_actual.observacion=  i['observacion']
                                    item_actual.save()                 
            
            elif action == 'editfinalizar':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    orientacion_academica = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='Finalizado').first()
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica anterior
                    #ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  -- logica actual
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    
                    #convertimos nuestras fechas en formato datetime 
                    fecha_hora_inicio = datetime.strptime(actividad_academica['datetime_inicio_estimado'], '%Y-%m-%d %H:%M:%S')
                    fecha_hora_fin = datetime.strptime(actividad_academica['datetime_fin_estimado'], '%Y-%m-%d %H:%M:%S')
                    #obtener las instancias de los objectos 
                    ins_convocatoria= Convocatoria.objects.get(id_convocatoria= actividad_academica['convocatoria'])
                    ins_facultad= Facultad.objects.get(id_facultad= actividad_academica['id_facultad'])
                    ins_func_doc_encargado= FuncionarioDocente.objects.get(id_funcionario_docente= actividad_academica['id_funcionario_docente_encargado'])
                    
                    #el estado se mantiene igual
                    #orientacion_academica.id_estado_actividad_academica = id_estado
                    #consultamos si la materia existe
                    ins_materia= None
                    if (actividad_academica['id_materia'] != ''):
                        ins_materia= Materia.objects.get(id_materia= actividad_academica['id_materia'])
                        orientacion_academica.id_materia= ins_materia 
                    #el estado se cambia
                    orientacion_academica.id_estado_actividad_academica = id_estado
                    orientacion_academica.id_departamento= ins_departamento
                    orientacion_academica.id_convocatoria = ins_convocatoria
                    orientacion_academica.id_facultad= ins_facultad
                    orientacion_academica.id_materia= ins_materia
                    orientacion_academica.id_funcionario_docente_encargado= ins_func_doc_encargado
                    #la persona se mantiene
                    #tutoria.id_persona_alta= ins_persona
                    dict = model_to_dict(request.user)
                    orientacion_academica.id_persona_ultima_modificacion= Persona.objects.get(pk= dict["id_persona"])
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_real= datetime.now()
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    orientacion_academica.nro_curso= actividad_academica['nro_curso']
                    orientacion_academica.observacion= actividad_academica['observacion']
                    orientacion_academica.save()
                    
                    #traemos la instancia de la actividad academica
                    ins_actividad_academica= Event.objects.get(id_actividad_academica= orientacion_academica.id_actividad_academica)
                    
                    #tambien modificamos el modelo hijo de ori academica
                    ori_academ_hijo = OrientacionAcademica.objects.get(id_orientacion_academica = self.get_object().id_actividad_academica)
                    ins_tipo_orientacion_academica= TipoOrientacionAcademica.objects.get(id_tipo_orientacion_academica= actividad_academica['id_tipo_orientacion_academica'])
                    ins_motivo_orientacion_academica= Motivo.objects.get(id_motivo= actividad_academica['id_motivo_ori_academ'])
                    ori_academ_hijo.id_tipo_orientacion_academica= ins_tipo_orientacion_academica
                    ori_academ_hijo.id_motivo = ins_motivo_orientacion_academica
                    ori_academ_hijo.save()
                    
                    #eliminamos todos los detalles de participantes
                    for i in DetalleActividadAcademica.objects.filter(id_actividad_academica= self.get_object().id_actividad_academica):
                        i.delete()
                        
                    # #guardamos el detalle de participantes
                    for i in actividad_academica['participantes']:
                        det_acti = DetalleActividadAcademica()
                        det_acti.id_actividad_academica= ins_actividad_academica
                        #obtenemos el id persona del participante
                        ins_participante= Persona.objects.get(id= i['id'])
                        det_acti.id_participante= ins_participante
                        det_acti.save()
                    
                    #obtenemos la persona que esta dando de alta 
                    current_user = request.user
                    dict = model_to_dict(current_user)
                    id_persona=  dict["id_persona"]
                    ins_persona= Persona.objects.get(id= id_persona)                    
                    
                   #guardamos las tareas
                    if actividad_academica['tareas']:
                            for i in actividad_academica['tareas']:
                                #por cada elemento consultamos el valor del id para comprobar si se trata de una tarea nueva o de una actualizacion de registro
                                
                                #se trata de un nuevo registro
                                if i['id'] == "":
                                    tarea = Tarea()
                                    tarea.id_persona_alta= ins_persona
                                    tarea.id_orientacion_academica= ori_academ_hijo
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    tarea.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    tarea.id_tipo_tarea= ins_tipo_tarea
                                    ins_responsable= Persona.objects.get(id= i['responsable'])
                                    #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_finalizacion= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                        tarea.id_persona_finalizacion= ins_responsable
                                        
                                    #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')
                                    #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        tarea.datetime_inicio_estimado= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_inicio_real= datetime.strptime(i['inicio'], '%Y-%m-%d %H:%M:%S')
                                        tarea.datetime_vencimiento= datetime.strptime(i['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                                    
                                    tarea.id_persona_responsable= ins_responsable
                                    tarea.datetime_alta= datetime.now()
                                    tarea.id_persona_ultima_modificacion= ins_persona
                                    tarea.observacion=  i['observacion']
                                    tarea.save()
                                    
                                else: #se trata de un registro ya existente
                                    #obtenemos el registro de la tarea para poder actualizar
                                    item_actual= Tarea.objects.filter(id_tarea= i['id']).first()
                                    #pisamos los campos
                                    ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= i['estado'])
                                    item_actual.id_estado_tarea= ins_estado_tarea
                                    ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= i['tipo_tarea'])
                                    item_actual.id_tipo_tarea= ins_tipo_tarea
                                    
                                    #si la tarea ya esta finalizada
                                    if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                                        if item_actual.datetime_inicio_real is None:
                                            item_actual.datetime_inicio_real= datetime.now()
                                        item_actual.datetime_finalizacion= datetime.now()
                                        item_actual.id_persona_finalizacion= ins_persona
                                        
                                    #si la tarea esta iniciada
                                    elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                                        item_actual.datetime_inicio_real= datetime.now()      
                                            
                                    item_actual.id_persona_ultima_modificacion= ins_persona
                                    item_actual.observacion=  i['observacion']
                                    item_actual.save()                  
                
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_datos_event(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ
            ins_evet = Event.objects.get(id_actividad_academica= self.get_object().id_actividad_academica)
            id_estado_actividad_academica= ins_evet.id_estado_actividad_academica.id_estado_actividad_academica
            id_convocatoria= ins_evet.id_convocatoria.id_convocatoria
            id_facultad= ins_evet.id_facultad.id_facultad
            if ins_evet.id_materia:
                id_materia= ins_evet.id_materia.id_materia
            else:
                id_materia= ''
            id_departamento= ins_evet.id_departamento.id_departamento
            id_funcionario_docente_encargado= ins_evet.id_funcionario_docente_encargado.id_funcionario_docente.id
            if ins_evet.id_persona_solicitante:
                id_persona_solicitante= ins_evet.id_persona_solicitante.id
            else:
                id_persona_solicitante= ''
            id_persona_alta= ins_evet.id_persona_alta.id
            datetime_inicio_estimado= ins_evet.datetime_inicio_estimado.strftime('%d-%m-%Y %H:%M:%S')
            datetime_fin_estimado = ins_evet.datetime_fin_estimado.strftime('%d-%m-%Y %H:%M:%S')
            if ins_evet.datetime_inicio_real:
                datetime_inicio_real = ins_evet.datetime_inicio_real.strftime('%d-%m-%Y %H:%M:%S')
            else:
                datetime_inicio_real = ''
            if ins_evet.datetime_fin_real:
                datetime_fin_real = ins_evet.datetime_fin_real.strftime('%d-%m-%Y %H:%M:%S')
            else:
                datetime_fin_real = ''
            datetime_registro = ins_evet.datetime_registro.strftime('%d-%m-%Y %H:%M:%S')
            if ins_evet.observacion is None:
                observacion= ''
            else:
                observacion= ins_evet.observacion
            if ins_evet.nro_curso is None: 
                nro_curso=''
            else:
                nro_curso= ins_evet.nro_curso
                
            auxiliar= {'id_estado_actividad_academica': id_estado_actividad_academica, 'id_convocatoria': id_convocatoria, 
            'id_facultad': id_facultad, 'id_materia': id_materia, 'id_departamento': id_departamento, 'id_funcionario_docente_encargado': id_funcionario_docente_encargado, 
            'id_persona_solicitante': id_persona_solicitante, 'id_persona_alta': id_persona_alta, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_fin_estimado': datetime_fin_estimado,
            'datetime_fin_estimado':datetime_fin_estimado, 'datetime_inicio_real': datetime_inicio_real, 'datetime_fin_real': datetime_fin_real, 'datetime_registro': datetime_registro, 'observacion': observacion, 'nro_curso': nro_curso}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            
        return data
    
    def get_datos_ori_academica(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ ori academ
            ins_orientacion_academica = OrientacionAcademica.objects.filter(id_orientacion_academica= self.get_object().id_actividad_academica).first()
            id_motivo = ins_orientacion_academica.id_motivo.id_motivo
            id_tipo_orientacion_academica = ins_orientacion_academica.id_tipo_orientacion_academica.id_tipo_orientacion_academica
            auxiliar= {'id_motivo': id_motivo, 'id_tipo_orientacion_academica': id_tipo_orientacion_academica}
            data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data

    def get_details_participantes(self):
        data = []
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_actividad_academica).values('id_participante')
            participantes= list(participantes)
            for i in participantes:
                id= i['id_participante']
                #obtenemos la persona
                id_persona= Persona.objects.get(id= id)
                item= id_persona.toJSON()
                item['value'] = id_persona.nombre + ' ' + id_persona.apellido
                data.append(item)
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_datos_tareas(self):
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ orientacion academica
            tareas = Tarea.objects.filter(id_orientacion_academica= self.get_object().id_actividad_academica)
            tareas_lista = list(tareas)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea.id_tarea
                    if tarea.id_persona_finalizacion:
                        id_persona_finalizacion = tarea.id_persona_finalizacion.id
                        persona_finalizacion= tarea.id_persona_finalizacion.nombre + ' ' + tarea.id_persona_finalizacion.apellido
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea.id_persona_alta.id
                    persona_alta= tarea.id_persona_alta.nombre + ' ' + tarea.id_persona_alta.apellido
                    if tarea.id_persona_responsable:
                        id_persona_responsable = tarea.id_persona_responsable.id
                        persona_responsable= tarea.id_persona_responsable.nombre + ' ' + tarea.id_persona_responsable.apellido
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    id_orientacion_academica = tarea.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                    id_estado_tarea = tarea.id_estado_tarea.id_estado_tarea
                    estado_tarea= tarea.id_estado_tarea.descripcion_estado_tarea
                    id_tipo_tarea = tarea.id_tipo_tarea.id_tipo_tarea
                    tipo_tarea= tarea.id_tipo_tarea.descripcion_tipo_tarea
                    datetime_inicio_estimado = tarea.datetime_inicio_estimado.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_inicio_real:
                        datetime_inicio_real = tarea.datetime_inicio_real.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = tarea.datetime_vencimiento.strftime('%Y-%m-%d %H:%M:%S')
                    datetime_alta = tarea.datetime_alta.strftime('%Y-%m-%d %H:%M:%S')
                    if tarea.datetime_finalizacion:
                        datetime_finalizacion = tarea.datetime_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion = tarea.datetime_ultima_modificacion.strftime('%Y-%m-%d %H:%M:%S')
                    observacion = tarea.observacion
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_orientacion_academica': id_orientacion_academica, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion}                    
                    data.append(auxiliar)                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Orientación Académica'
        context['entity'] = 'Orientación Académica'
        context['list_url'] = self.success_url
        context['det'] = json.dumps(self.get_details_participantes())
        context['orientacion'] = json.dumps(self.get_datos_ori_academica())
        context['event'] = self.get_datos_event()
        context['tarea'] = self.get_datos_tareas()
        return context
    
class TareasView(LoginRequiredMixin, ListView):
    #login_url = "accounts:signin"
    model = Tarea
    template_name = 'calendarapp/tareas_list.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_datos_tareas(self):
        
        data = []
        try:
            #obtenemos todos los datos de la instancia acti academ tutoria
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            tareas = Tarea.objects.all().filter(id_persona_responsable= ins_persona)#filter(id_tutoria= self.get_object().id_actividad_academica)
            # Convertir el queryset a JSON en formato de cadena (str)
            tareas_lista= serializers.serialize('json', tareas)
            # Convertir la cadena JSON a un diccionario
            tareas_lista = json.loads(tareas_lista)
            if tareas_lista:
                for tarea in tareas_lista:
                    id_tarea = tarea['pk']
                    if tarea['fields']['id_persona_finalizacion']:
                        id_persona_finalizacion = tarea['fields']['id_persona_finalizacion']
                        persona_finalizacion=  Persona.objects.filter(id= id_persona_finalizacion).values('nombre', 'apellido').first()
                        persona_finalizacion= persona_finalizacion['nombre'] + ' ' + persona_finalizacion['apellido']
                    else:
                        id_persona_finalizacion= ''
                        persona_finalizacion= ''
                    id_persona_alta = tarea['fields']['id_persona_alta']
                    persona_alta= Persona.objects.filter(id= id_persona_alta).values('nombre', 'apellido').first()
                    persona_alta= persona_alta['nombre'] + ' ' + persona_alta['apellido']
                    if tarea['fields']['id_persona_responsable']:
                        id_persona_responsable = tarea['fields']['id_persona_responsable']
                        persona_responsable= Persona.objects.filter(id= id_persona_responsable).values('nombre', 'apellido').first()
                        persona_responsable= persona_responsable['nombre'] + ' ' + persona_responsable['apellido']
                    else: 
                        id_persona_responsable= ''
                        persona_responsable= ''
                    if tarea['fields']['id_tutoria']:
                        id_tutoria = tarea['fields']['id_tutoria']
                    else:
                        id_tutoria = ''
                    if tarea['fields']['id_orientacion_academica']:
                        id_orientacion_academica = tarea['fields']['id_orientacion_academica']
                    else:
                        id_orientacion_academica = ''
                    id_estado_tarea = tarea['fields']['id_estado_tarea']
                    #traer la descripcion de la tarea
                    estado_tarea= EstadoTarea.objects.filter(id_estado_tarea= id_estado_tarea).values('descripcion_estado_tarea').first()
                    if estado_tarea['descripcion_estado_tarea'] not in ('Finalizada', 'Cancelada') and datetime.fromisoformat(tarea['fields']['datetime_vencimiento']) <= datetime.now():
                        estado_tarea= 'Vencida'
                    else:
                        estado_tarea= estado_tarea['descripcion_estado_tarea']
                    id_tipo_tarea = tarea['fields']['id_tipo_tarea']
                    tipo_tarea= TipoTarea.objects.filter(id_tipo_tarea= id_tipo_tarea).values('descripcion_tipo_tarea').first()
                    tipo_tarea= tipo_tarea['descripcion_tipo_tarea']
                    datetime_inicio_estimado = datetime.fromisoformat(tarea['fields']['datetime_inicio_estimado']).strftime('%d-%m-%Y %H:%M:%S')
                    if tarea['fields']['datetime_inicio_real']:
                        datetime_inicio_real= datetime.fromisoformat(tarea['fields']['datetime_inicio_real']).strftime('%d-%m-%Y %H:%M:%S')
                    else:
                        datetime_inicio_real= ''
                    datetime_vencimiento = datetime.fromisoformat(tarea['fields']['datetime_vencimiento']).strftime('%d-%m-%Y %H:%M:%S')
                    datetime_alta = datetime.fromisoformat(tarea['fields']['datetime_alta']).strftime('%d-%m-%Y %H:%M:%S')
                    if tarea['fields']['datetime_finalizacion']:
                        datetime_finalizacion = datetime.fromisoformat(tarea['fields']['datetime_finalizacion']).strftime('%d-%m-%Y %H:%M:%S')
                    else:
                        datetime_finalizacion= ''
                    datetime_ultima_modificacion =  datetime.fromisoformat(tarea['fields']['datetime_ultima_modificacion']).strftime('%d-%m-%Y %H:%M:%S')
                    observacion = tarea['fields']['observacion']
                    
                    auxiliar= {'id_tarea': id_tarea, 'id_persona_finalizacion': id_persona_finalizacion, 'persona_finalizacion': persona_finalizacion,
                    'id_persona_alta': id_persona_alta, 'persona_alta': persona_alta, 'id_persona_responsable': id_persona_responsable, 'persona_responsable': persona_responsable, 'id_tutoria': id_tutoria, 
                    'id_estado_tarea': id_estado_tarea, 'estado_tarea': estado_tarea, 'tipo_tarea': tipo_tarea, 'id_tipo_tarea': id_tipo_tarea, 'datetime_inicio_estimado': datetime_inicio_estimado, 'datetime_inicio_real': datetime_inicio_real,
                    'datetime_vencimiento':datetime_vencimiento, 'datetime_alta': datetime_alta, 'datetime_finalizacion': datetime_finalizacion, 
                    'datetime_ultima_modificacion': datetime_ultima_modificacion, 'observacion': observacion, 'id_orientacion_academica': id_orientacion_academica}               
                    data.append(auxiliar)    
                    
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
    def get_tareas_medicion(self):
        data = {}
        try:
             #obtenemos todos los datos de la instancia acti academ tutoria
            request = self.request
            current_user= request.user
            dict = model_to_dict(current_user)
            ins_persona=  Persona.objects.get(id= dict["id_persona"])
            tareas= Tarea.objects.all().filter(id_persona_responsable= ins_persona).order_by('-datetime_inicio_estimado')
            #devolvemos solo aquellos registros que correspondan al usuario logeado
            tarea_finalizada=  tareas.filter(id_estado_tarea__descripcion_estado_tarea= 'Finalizada').count()
            tarea_iniciada =tareas.filter( id_estado_tarea__descripcion_estado_tarea= 'Iniciada').count()
            tarea_cancelada = tareas.filter(id_estado_tarea__descripcion_estado_tarea= 'Cancelada').count()
            tarea_vencida = tareas.filter(~Q(id_estado_tarea__descripcion_estado_tarea__in=['Cancelada', 'Finalizada']), datetime_vencimiento__lte=datetime.now()).count()
            tarea_pendiente = tareas.filter(id_estado_tarea__descripcion_estado_tarea= 'Pendiente').count()
            data= {'tarea_iniciada': tarea_iniciada, 'tarea_cancelada': tarea_cancelada, 'tarea_finalizada': tarea_finalizada, 'tarea_pendiente': tarea_pendiente, 'tarea_vencida': tarea_vencida}
        except Exception as e:
            print(f"Se ha producido un error: {e}")
        return data
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarea'] = json.dumps(self.get_datos_tareas())
        context['datos'] = self.get_tareas_medicion()
        return context


#metodo para anhadir una tarea 


@csrf_exempt
@login_required
def AddTarea(request):
    if request.method == "POST":                
            try:
                tarea= json.loads(request.POST['tarea'])
                #obtenemos la persona que esta dando de alta 
                current_user = request.user
                dict = model_to_dict(current_user)
                id_persona=  dict["id_persona"]
                ins_persona= Persona.objects.get(id= id_persona)
                record = Tarea()
                ins_ori_academ= ''
                ins_tutoria= ''
                record.id_persona_alta= ins_persona
                if tarea['tipo_actividad_academica'] == 'tutoria':
                    ins_tutoria= Tutoria.objects.get(id_tutoria= tarea['id_actividad_academica'])
                    record.id_tutoria= ins_tutoria
                else:
                    ins_ori_academ= OrientacionAcademica.objects.get(id_orientacion_academica= tarea['id_actividad_academica'])
                    record.id_orientacion_academica= ins_ori_academ
                    
                ins_estado_tarea= EstadoTarea.objects.get(id_estado_tarea= tarea['estado'])
                record.id_estado_tarea= ins_estado_tarea
                ins_tipo_tarea= TipoTarea.objects.get(id_tipo_tarea= tarea['tipo_tarea'])
                record.id_tipo_tarea= ins_tipo_tarea
                ins_responsable= Persona.objects.get(id= tarea['responsable'])
                #si la tarea ya esta finalizada, la fecha inicio estimado y real seran iguales y la fecha vencimiento sera igual a la finalizada
                if ins_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                    record.datetime_inicio_estimado= datetime.strptime(tarea['inicio'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_inicio_real= datetime.strptime(tarea['inicio'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_finalizacion= datetime.strptime(tarea['vencimiento'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_vencimiento= datetime.strptime(tarea['vencimiento'], '%Y-%m-%d %H:%M:%S')
                    record.id_persona_finalizacion= ins_responsable
                    
                #si la tarea esta pendiente aun no existira fecha real ni de finalizacion
                elif ins_estado_tarea.descripcion_estado_tarea == 'Pendiente':
                    record.datetime_inicio_estimado= datetime.strptime(tarea['inicio'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_vencimiento= datetime.strptime(tarea['vencimiento'], '%Y-%m-%d %H:%M:%S')
                #si la tarea esta iniciada tendra fecha real pero aun no la de finalizacion 
                elif ins_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                    record.datetime_inicio_estimado= datetime.strptime(tarea['inicio'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_inicio_real= datetime.strptime(tarea['inicio'], '%Y-%m-%d %H:%M:%S')
                    record.datetime_vencimiento= datetime.strptime(tarea['vencimiento'], '%Y-%m-%d %H:%M:%S')   
                
                record.id_persona_responsable= ins_responsable
                record.datetime_alta= datetime.now()
                record.id_persona_ultima_modificacion= ins_persona
                record.observacion=  tarea['observacion']
                record.save()
                
                data= json.dumps([{"name": 200}])
                return HttpResponse(data)

            except Exception as e:
                print(f"Se ha producido un error: {e}")
                data= json.dumps([{"name": 500}])
                return HttpResponse(data)
           
