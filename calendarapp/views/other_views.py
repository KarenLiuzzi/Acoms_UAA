# cal/views.py
import json
from turtle import title
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from calendarapp.models.event import DetalleActividadAcademica
import requests
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from calendarapp.forms import HorarioSemestralForm, ActividadAcademicaForm
from accounts.models.user import FuncionarioDocente, Persona, Materia, Departamento, User, Facultad
from calendarapp.models import EventMember, Event
from calendarapp.models.event import Parametro, Cita, EstadoActividadAcademica, Tutoria, Tarea ,OrientacionAcademica, EstadoTarea ,TipoTutoria, TipoTarea ,TipoOrientacionAcademica, Motivo
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime, timedelta, date, time
from django.core import serializers
import pandas as pd
from django.db.models import Q

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


# @login_required(login_url="signup")
# def create_event(request):
#     form = EventForm(request.POST or None)
#     if request.POST and form.is_valid():
#         title = form.cleaned_data["title"]
#         description = form.cleaned_data["description"]
#         start_time = form.cleaned_data["start_time"]
#         end_time = form.cleaned_data["end_time"]
#         Event.objects.get_or_create(
#             user=request.user,
#             title=title,
#             description=description,
#             start_time=start_time,
#             end_time=end_time,
#         )
#         return HttpResponseRedirect(reverse("calendarapp:calendar"))
#     return render(request, "event.html", {"form": form})


# class EventEdit(generic.UpdateView):
#     model = Event
#     fields = ["observacion", "datetime_inicio_estimado", "datetime_fin_estimado"]
#     template_name = "event.html"


# @login_required(login_url="signup")
# def event_details(request, event_id):
#     event = Event.objects.get(id_actividad_academica=event_id)
#     eventmember = EventMember.objects.filter(event=event)
#     context = {"event": event, "eventmember": eventmember}
#     return render(request, "event-details.html", context)


# def add_eventmember(request, event_id):
#     forms = AddMemberForm()
#     if request.method == "POST":
#         forms = AddMemberForm(request.POST)
#         if forms.is_valid():
#             member = EventMember.objects.filter(event=event_id)
#             event = Event.objects.get(id=event_id)
#             if member.count() <= 9:
#                 user = forms.cleaned_data["user"]
#                 EventMember.objects.create(event=event, user=user)
#                 return redirect("calendarapp:calendar")
#             else:
#                 print("--------------User limit exceed!-----------------")
#     context = {"form": forms}
#     return render(request, "add_member.html", context)


# class EventMemberDeleteView(generic.DeleteView):
#     model = EventMember
#     template_name = "event_delete.html"
#     success_url = reverse_lazy("calendarapp:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        #events = Event.objects.get_all_events(user=request.user)
        events = Event.objects.get_all_events()
        #events_month = Event.objects.get_running_events(user=request.user)
        events_month = Event.objects.get_running_events(tipo_cita= '')
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
                print(participantes)
            else:
                participantes= []

            
            #estos nombres tienen que mantenerse
            event_list.append(
                {
                    "title": event.id_cita.id_facultad.descripcion_facultad,
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
                    "participantes": participantes_lista
                }
                
            )
            #print(event.id_cita.id_actividad_academica)
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
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
# @login_required
# def ListCalendarioFuncDoc(request):
#     #obtenemos todos los objetos de horario semestral del funcionario docente y devolvemos en el template
#     #pasar solo los horarios semestrales que correspondan con el usuario logeado
#     current_user = request.user
#     #https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
#     dict = model_to_dict(current_user)
#     persona=  dict["id_persona"]
#     print(persona)
#     dict_cal_fun_doc= HorarioSemestral.objects.filter(id_funcionario_docente= persona)
#     #print(dict_cal_fun_doc)
#     context = { "dict_cal_fun_doc": dict_cal_fun_doc}
#     #return render(request,'calendarapp/lista_calendario.html',context=context)
#     return render(request,'calendarapp/calendario_form.html',context=context)

@login_required
def formCalendarioFuncDoc(request):
    #STO DEBO COMENTAR Y SACAR EL CONTEXT
    if request.method != "POST":
        current_user = request.user
        dict = model_to_dict(current_user)
        persona=  dict["id_persona"]
        dict_cal_fun_doc= HorarioSemestral.objects.filter(id_funcionario_docente= persona)
        context = { "dict_cal_fun_doc": dict_cal_fun_doc}
        return render(request,'calendarapp/calendario_form.html', context= context)

@login_required
def EditCalendarioFuncDoc(request, pk):
    hor_sem= get_object_or_404(HorarioSemestral, id_horario_semestral= pk)
    if request.method == "POST":
        #modiicar el form
        form = HorarioSemestralForm(request.POST, instance=hor_sem, user=request.user)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse("calendarapp:form_cal_func_doc"), status=200)
            return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro Modificado."})})
             #, status=204, headers={'HX-Trigger': json.dumps({"showMessage": "Registro Modificado."})})
            
        #else:
            #messages.error(request, 'Los datos son incorrectos, vuelve a intentarlo.')
    else:
        form= HorarioSemestralForm(instance= hor_sem, user=request.user)
    
    #modificar el html
    return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form, "hor_sem": hor_sem})

@login_required
def AddCalendarioFuncDoc(request):
    
    if request.method == "POST":
        #modificar el form
        # func_doc= FuncionarioDocente.objects.get(id_funcionario_docente= request.user.id_persona)
        # print( form.id_funcionario_docente)
        # form.id_funcionario_docente = func_doc 
        # print(form.id_funcionario_docente)  # Asignamos el funcionario/docente autenticado al campo 'id_funcionario_docente'
        # print('antes el if')
        form = HorarioSemestralForm(request.POST, user=request.user)
        # print(form.fields['id_funcionario_docente'])
        # form.fields['id_funcionario_docente'] = FuncionarioDocente.objects.get(id_funcionario_docente= request.user.id_persona)
        # print(form.fields['id_funcionario_docente'])
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro agregado."})})
            #return HttpResponseRedirect(reverse("calendarapp:form_cal_func_doc"))
            #return HttpResponseRedirect(reverse("calendarapp:form_cal_func_doc"), status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro Modificado."})})
        #else: 
           #messages.error(request, 'Los datos son incorrectos, vuelve a intentarlo.')
    else:
        form = HorarioSemestralForm(user=request.user)
    return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form})

# def delFormCalendrioFuncDoc(request, pk):
#     context= {"pk": pk}
#     return render(request, "/eliminar_arcivo.html", context)

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
                #return HttpResponseRedirect(reverse("calendarapp:form_cal_func_doc"))
                #return HttpResponseRedirect(reverse("calendarapp:form_cal_func_doc"), status=204, headers={'HX-Trigger': json.dumps({"calenarioListChange": None, "showMessage": "Registro Modificado."})})
            
            except:
                messages.error(request, 'Ocurrió un error al intentar eliminar el registro.')
                # Eliminar todos los mensajes de error
                # storage = messages.get_messages(request)
                # for message in storage:
                #     if message.level == messages.ERROR:
                #         storage.discard(message)
                return render(request, "eliminar_registro.html", context = {"pk": pk})
                
                
    else:
        
        return render(request, "eliminar_registro.html", context = {"pk": pk})

    #ver como hacer aqui
    #return render(request, "calendarapp/form_hora_sem_func_doc.html")


#agregados de pruebas

def tipo_cita(request):
    return render(request,'calendarapp/tipo_cita.html')

def tipo_acti_academ(request):
    return render(request,'calendarapp/tipo_actividad_academica.html')

def ori_academica(request):
    return render(request,'calendarapp/prueba_ori_academica.html')

from django.http import JsonResponse

def actualizar_campo(request):
    
    campo = request.GET.get('campo')
    
    if campo == "facultad":
        queryset= ""
        queryset = Facultad.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_facultad}">{item.descripcion_facultad}</option>'
            
    elif campo == "materia":
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
            
    elif campo == "funcionariodocente":
        
        selected_option= ""
        selected_option = request.GET.get('id_materia')
        
        #obtenemos el funcionario docente de la materia seleccionada
        queryset= ""
        #tengo que obtener el id de la materia y traer el usuario que tenga una relacion con esa materia
        materia= Materia.objects.get(id_materia= selected_option)
        usuarios_relacionados= materia.func_doc_materias.all().values('id')
        funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente__in=usuarios_relacionados).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
        queryset= funcionario_docente

        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            #options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.id_funcionario_docente.nombre} {item.id_funcionario_docente.id_funcionario_docente.apellido}</option>'
             options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
    
    elif campo == 'todos_funcionarios_docentes':
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
        queryset= ""
        queryset = TipoTutoria.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_tipo_tutoria}">{item.descripcion_tipo_tutoria}</option>'
            
    elif campo == "tipo_ori_academ":
        queryset= ""
        queryset = TipoOrientacionAcademica.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_tipo_orientacion_academica}">{item.descripcion_tipo_orientacion_academica}</option>'
            
    elif campo == "motivo_ori_academ":
        
        selected_option= ""
        selected_option = request.GET.get('selected_option')
        
        queryset= ""
        #traer todos los motivos de acuerdo al tipo de orientacion academica
        queryset = Motivo.objects.filter(id_tipo_orientacion_academica= selected_option)
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_motivo}">{item.descripcion_motivo}</option>'        
            
    elif campo == "materias": 
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
    
    elif campo == "funcionariodocente_logeado": #usado para el add de tutoria
        
        #obtenemos el usuario que solicita
        current_user = request.user
        
        #traemos el id del func_doc
        queryset= ""
        funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente= current_user.id).values('id_funcionario_docente', 'id_funcionario_docente__nombre', 'id_funcionario_docente__apellido')
        queryset= funcionario_docente

        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item["id_funcionario_docente"]}">{item["id_funcionario_docente__nombre"]} {item["id_funcionario_docente__apellido"]}</option>'
    
        
    # elif campo == "funcdoc_logeado_materias": #usado para el add de tutoria
        
    #     selected_option= ""
    #     selected_option = request.GET.get('func_doc')
    #     #obtenemos primeramente el departamento asignado al funcionario logeado
    #     departamentos =  FuncionarioDocente.objects.filter(id_funcionario_docente= selected_option).values("id_departamento")
    #     queryset= Materia.objects.filter(id_departamento__in = departamentos)
        
    #     # Pasar los datos del queryset a datos HTML
    #     options = ''
    #     for item in queryset:
    #         options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
    
    elif campo == "funcdoc_logeado_materias": #usado para el add de tutoria
        
        selected_option= ""
        selected_option = request.GET.get('func_doc')
        #obtenemos las materias asignadas al usuario actual
        usuario =  User.objects.filter(id= selected_option).first()
        materias_asignadas = usuario.materia_func_doc.all()
        queryset= Materia.objects.filter(id_materia__in = materias_asignadas)
        
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_materia}">{item.descripcion_materia}</option>'
    
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
            
    if campo == "personas":
     
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
                 
                 
    if campo == "tipo_tareas":
        
        queryset= TipoTarea.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_tipo_tarea}">{item.descripcion_tipo_tarea} </option>'    
            
    if campo == "estado_tareas":
        
        queryset= EstadoTarea.objects.all()
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            options += f'<option value="{item.id_estado_tarea}">{item.descripcion_estado_tarea} </option>'            
    
                
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
    

    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_cita)
            data= participantes      
        except:
            pass
        return data
    
    def get_details_orientacion_academica(self):
        data = OrientacionAcademica.objects.none()
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            orientacion_academica= OrientacionAcademica.objects.filter(id_orientacion_academica=self.get_object().id_cita).first()
            data= orientacion_academica
                    
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Cita de Orientación Académica'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['orientacion_academica'] =  self.get_details_orientacion_academica()
        return context

#clase de vista de cita de tipo tutoria
class CitaTutoriaDetalle(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'calendarapp/detalles_cita_tutoria.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'cita'
    

    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_cita)
            data= participantes      
        except:
            pass
        return data
    
    def get_details_tutoria(self):
        data = Tutoria.objects.none()
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            tutoria= Tutoria.objects.filter(id_tutoria=self.get_object().id_cita)
            data= tutoria
                    
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Cita de Tutoría'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['tutoria'] =  self.get_details_tutoria()
        return context  

#clase de vista de tipo orientacion academica
class OrientacionAcademicaDetalle(LoginRequiredMixin, DetailView):
    model = OrientacionAcademica
    template_name = 'calendarapp/detalles_cita_orientacion_academica.html'
    #permission_required = 'erp.view_sale'
    context_object_name= 'orientacion_academica'
    queryset= OrientacionAcademica.objects.select_related("id_orientacion_academica")
    
    def get_tareas(self):
        data = Tarea.objects.none()
        try:
            orientacion_academica= Tarea.objects.filter(id_orientacion_academica=self.get_object().id_orientacion_academica)
            data= orientacion_academica
        except:
            pass
        return data
    
    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_orientacion_academica)
            data= participantes      
        except:
            pass
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
    
    def get_tareas(self):
        data = {}
        try:
            tarea= Tarea.objects.filter(id_tutoria= self.get_object())            
            data= tarea
        except:
            pass
        
        return data
    
    def get_details_participantes(self):
        data = {}
        try:
            #obtenemos todos los id de los participantes y devolvemos los datos de la tabla persona
            participantes= DetalleActividadAcademica.objects.filter(id_actividad_academica=self.get_object().id_tutoria)
            data= participantes      
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Tutoría'
        #context['modificar_url'] = reverse_lazy('erp:sale_create')
        context['participantes'] =  self.get_details_participantes()
        context['tareas'] =  self.get_tareas()
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
                    id_parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').first()
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
                    id_parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').first()
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
                    cita.id_persona_alta= ins_persona
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
        except:
            pass
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
                
        except:
            pass
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
            
        except:
            pass
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
                    cita.id_persona_alta= ins_persona
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
        except:
            pass
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
                
        except:
            pass
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
            
        except:
            pass
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
class CitaTutoriaIniciarView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/iniciar_cita_tutoria.html'
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
        except:
            pass
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
                
        except:
            pass
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
class CitaOrientacionAcademicaIniciarView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/iniciar_cita_orientacion_academica.html'
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
            elif action == 'iniciar':
                with transaction.atomic():
                    actividad_academica = json.loads(request.POST['actividad_academica'])
                    cita = self.get_object() #obtenemos la instancia del objecto
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='finalizado').first()
                    
                    #buscamos el primer departamento el cual esta asociado la facultad -- esto con la logica actual
                    ins_departamento =  Departamento.objects.filter(id_facultad= actividad_academica['id_facultad']).first()
                    
                    ''' con la logica posterior
                    #buscamos el primer departamento al cual esta asociado el funcionario docente  
                    dep_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente = actividad_academica['id_funcionario_docente_encargado']).values("id_departamento").first()
                    dep_func_doc= dep_func_doc["id_departamento'"]
                    ins_departamento=  Departamento.objects.get(id_departamento= dep_func_doc)
                    '''
                    
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
        except:
            pass
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
                
        except:
            pass
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
    
    #el parametro cargaremos en minutos y ese vamos a tomar como valor para poder calcular el tiempo entre horarios del funcionario/docente
    #/*************************Inicio funcion para generar los horarios****************************************/
    def dividir_horarios_por_minuto(minutos, hora_inicio, hora_fin, dia, id_convocatoria):
        # Convertir los horarios de strings a objetos datetime
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
        hora_fin = datetime.strptime(hora_fin, '%H:%M:%S').time()

        # Calcular la diferencia en minutos entre la hora de inicio y fin
        diferencia = timedelta(hours=hora_fin.hour, minutes=hora_fin.minute) - timedelta(hours=hora_inicio.hour, minutes=hora_inicio.minute)
        minutos_totales = int(diferencia.total_seconds() / 60)

        # Dividir la diferencia en minutos según el parámetro "minutos"
        divisiones = []
        for i in range(minutos, minutos_totales + minutos, minutos):
            hora_inicio_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i-minutos)).time()
            hora_fin_division = (datetime.combine(datetime.today(), hora_inicio) + timedelta(minutes=i)).time()

            if(hora_fin_division <= hora_fin):
                divisiones.append({"hora_inicio": hora_inicio_division, "hora_fin":hora_fin_division, "dia": dia, "id_convocatoria": id_convocatoria})

        return divisiones

    #/*****************************Fin funcion para generar los horarios****************************************/

    '''El campo de parametro cargaremos en minutos y ese vamos a tomar como valor para poder calcular el tiempo de proceso entre horarios del 
    funcionario/docente primero traemos el parametro de minutos que se encuentra disponible de acuerdo a la actividad academica (tuto u orie academ ) '''

    if tipo== "tutoria":
        parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
        parametro= parametro[0]['valor']
        
    elif tipo== "ori_academica":
        parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
        parametro= parametro[0]['valor']
    else:
        parametro= 0

    #vamos a consultar los horarios cargados del funcionario_docente solicitado cuyo semestre aun no haya finalizado    
    horario_func_doc= HorarioSemestral.objects.filter(id_funcionario_docente= func_doc, id_convocatoria__fecha_fin__gt = datetime.now())
    # Convertir el queryset a JSON en formato de cadena (str)
    horario_func_doc= serializers.serialize('json', horario_func_doc)
    
    # Convertir la cadena JSON a un diccionario
    horario_func_doc = json.loads(horario_func_doc)

    
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
        #agregar columna de Mes
        df2['mes'] = df2['fecha'].apply(lambda x: meses_espanol[x.month])
        
        # Formatear la columna 'fecha' con el formato 'dd-mm-yyyy'
        df2['fecha'] = df2['fecha'].apply(lambda x: x.strftime('%d-%m-%Y'))
        
        horarios_disponibles= df2
        
    # caso si el fun/doc no tiene ningun calendario disponible devolver resultado vacio
    elif (df2.empty):
        horarios_disponibles= pd.DataFrame()
        
    #Finalmente devolvemos un JSON 
    #horarios_disponibles.to_excel("C:/Users/beatr/Documents/horarios_disponibles.xlsx", index=False)

    '''El método to_json() también admite otros formatos de orientación, como 'split', 'index', 'columns', 'values' y 'table', para adaptarse 
    a diferentes necesidades de estructura JSON. Puedes revisar la documentación de pandas para obtener más detalles sobre estos formatos.'''
    horarios_disponibles= horarios_disponibles.to_json(orient='records')
    
    
    # print(type(horarios_disponibles))
    # print(horarios_disponibles)

    return JsonResponse(horarios_disponibles, safe=False)


#clase de creacion para una actividad academica de tipo tutoria
class TutoriaCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/tutoria_create.html'
    success_url = 'running-acti_academ-list/Tutoria/' #reverse_lazy('calendarapp:calenders')
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
                    tutoria.id_persona_solicitante= ins_solicitante
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    #tutoria.datetime_inicio_real= fecha_hora_inicio
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
                    tutoria.id_persona_solicitante= ins_solicitante
                    tutoria.datetime_inicio_estimado= fecha_hora_inicio
                    tutoria.datetime_fin_estimado= fecha_hora_fin
                    tutoria.datetime_inicio_real= fecha_hora_inicio
                    tutoria.datetime_fin_real= fecha_hora_fin
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
class OrientacionAcademicaCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/orientacion_academica_create.html'
    success_url = 'running-acti_academ-list/OriAcademica/' #reverse_lazy('calendarapp:calenders')
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
                    orientacion_academica = Event()
                    #buscamos el id del estado pendiente
                    id_estado= EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains='iniciada').first()
                    
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
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    #orientacion_academica.datetime_inicio_real= fecha_hora_inicio
                    #orientacion_academica.datetime_fin_real= fecha_hora_fin
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
                    orientacion_academica.datetime_inicio_estimado= fecha_hora_inicio
                    orientacion_academica.datetime_fin_estimado= fecha_hora_fin
                    orientacion_academica.datetime_inicio_real= fecha_hora_inicio
                    orientacion_academica.datetime_fin_real= fecha_hora_fin
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