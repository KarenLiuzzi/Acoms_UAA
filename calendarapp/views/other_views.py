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
from calendarapp.models.calendario import HorarioSemestral
from calendarapp.forms import HorarioSemestralForm, ActividadAcademicaForm
from accounts.models.user import FuncionarioDocente, Persona, Materia, Departamento, User, Facultad
from calendarapp.models import EventMember, Event
from calendarapp.models.event import Parametro
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime, timedelta

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


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["observacion", "datetime_inicio_estimado", "datetime_fin_estimado"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id_actividad_academica=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendarapp:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")


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
            receptor= ""
            if event.id_cita.id_persona_receptor:
                receptor= event.id_cita.id_persona_receptor.nombre + ' ' + event.id_cita.id_persona_receptor.apellido
            else:
                receptor= "----------"
                
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
                    "receptor": receptor, 
                    "estado": estado, 
                    "convocatoria":convocatoria, 
                    "facultad": facultad, 
                    "materia":materia, 
                    "observacion":observacion, 
                    "curso": curso,
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

@login_required
def tutoria(request):
    if request.method == "GET":
        form = ActividadAcademicaForm() 
    
    # else:
    #     if form.is_valid():
    #         # Obtener opciones del campo2 usando cargar_opciones
    #         departamento = cargar_opciones(request)

    #         # Actualizar el campo select en el formulario con las opciones
    #         form.fields['departamento'].choices = [(opcion['value'], opcion['label']) for opcion in departamento]

    #         # Actualizar el queryset del campo2 en el formulario
    #         form.fields['facultad'].queryset = opciones_departamento
  
    return render(request,'calendarapp/form_cita_tutoria.html', {'form': form})

def tipo_cita(request):
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
        funcionario_docente=  FuncionarioDocente.objects.filter(id_funcionario_docente__in=usuarios_relacionados)
        queryset= funcionario_docente

        
        # Pasar los datos del queryset a datos HTML
        options = ''
        for item in queryset:
            #options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.id_funcionario_docente.nombre} {item.id_funcionario_docente.id_funcionario_docente.apellido}</option>'
             options += f'<option value="{item.id_funcionario_docente}">{item.id_funcionario_docente.nombre} {item.id_funcionario_docente.apellido}</option>'

    return JsonResponse(options, safe=False)

def obtener_horarios_cita(request):
    
    tipo = request.GET.get('tipo_acti_academica')
    func_doc = request.GET.get('id_func_doc')
    #el parametro cargaremos en minutos y ese vamos a tomar como valor para poder calcular el tiempo entre horarios del funcionario/docente

    #logica para obtener los horarios disponibles del funcionario/docente de acuerdo al horario del mismo y si este rango de horarios aun se 
    #encuentra disponible
    
    #primero traemos el parametro de minutos que se encuentra disponible de acuerdo a la actividad academica (tuto u orie academ )
    if tipo== "tutoria":
        parametro = Parametro.objects.filter(es_tutoria= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
    elif tipo== "ori_academica":
        parametro = Parametro.objects.filter(es_orientacion_academica= True, id_unidad_medida__descripcion_unidad_medida__contains='minutos').values('valor')
    else:
        parametro= ""
    
    #vamos a consultar los horarios cargados del funcionario_docente cuyo semestre aun no haya finalizado
    horario_func_doc= HorarioSemestral.objects.filter(id_funcionario_docente= func_doc, id_convocatoria__fecha_fin__gt=datetime.now())
    
        
def dividir_fechas_en_minutos(fecha1, fecha2, minutos):
    # Convertir las fechas de strings a objetos datetime
    fecha1 = datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
    fecha2 = datetime.strptime(fecha2, '%Y-%m-%d %H:%M:%S')

    # Calcular la diferencia en minutos
    diferencia = fecha2 - fecha1
    minutos_totales = int(diferencia.total_seconds() / 60)

    # Dividir la diferencia en minutos según el tercer parámetro
    divisiones = []
    for i in range(minutos, minutos_totales + minutos, minutos):
        fecha_division = fecha1 + timedelta(minutes=i)
        divisiones.append(fecha_division)

    return divisiones


    
    return JsonResponse(results, safe=False)

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


class ActividadAcademicaCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = ActividadAcademicaForm
    template_name = 'calendarapp/actividad_academica_create.html'
    success_url = reverse_lazy('calendarapp:calenders')
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
            # elif action == 'search_facultad':
            #     data = []
            #     facultades = Facultad.objects.all()
            #     for i in facultades:
            #         item = i.toJSON()
            #         item['value'] = i.descripcion_facultad
            #         data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    print('entro')
                    # actividad_academica = json.loads(request.POST['actividad_academica'])
                    # cita = Event()
                    # cita.date_joined = actividad_academica['date_joined']
                    # cita.cli_id = actividad_academica['cli']
                    # cita.subtotal = float(actividad_academica['subtotal'])
                    # cita.iva = float(actividad_academica['iva'])
                    # cita.total = float(actividad_academica['total'])
                    # cita.save()
                    # for i in vents['products']:
                    #     det = DetSale()
                    #     det.sale_id = sale.id
                    #     det.prod_id = i['id']
                    #     det.cant = int(i['cant'])
                    #     det.price = float(i['pvp'])
                    #     det.subtotal = float(i['subtotal'])
                    #     det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Cita'
        context['entity'] = 'Actividad Academica'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context