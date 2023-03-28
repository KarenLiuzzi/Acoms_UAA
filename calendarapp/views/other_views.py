# cal/views.py

from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from calendarapp.models.calendario import HorarioSemestral
from calendarapp.forms import HorarioSemestralForm
from accounts.models.user import FuncionarioDocente
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm


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
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
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
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
    
#-------------------------------Función ABM Horario Semestral Funcionario/docente------------------------------------

def ListCalendarioFuncDoc(request):
    print("hace el llamado")
    #obtenemos todos los objetos de horario semestral del funcionario docente y devolvemos en el template
    #pasar solo los horarios semestrales que correspondan con el usuario logeado
    current_user = request.user
    #https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
    dict = model_to_dict(current_user)
    persona=  dict["id_persona"]
    print(persona)
    dict_cal_fun_doc= HorarioSemestral.objects.filter(id_funcionario_docente= persona)
    context = { "dict_cal_fun_doc": dict_cal_fun_doc}
    return render(request,'calendarapp/lista_calendario.html',context=context)

def formCalendarioFuncDoc(request):
    return render(request,'calendarapp/calendario_form.html')

def EditCalendarioFuncDoc(request, pk):
    hor_sem= get_object_or_404(HorarioSemestral, id_horario_semestral= pk)
    if request.method == "POST":
        #modiicar el form
        form = HorarioSemestralForm(request.POST, instance=hor_sem, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'calenarioListChange'})
        #else:
            #messages.error(request, 'Los datos son incorrectos, vuelve a intentarlo.')
    else:
        form= HorarioSemestralForm(instance= hor_sem, user=request.user)
    
    #modificar el html
    return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form, "hor_sem": hor_sem})

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
            return HttpResponse(status=204, headers={'HX-Trigger': 'calenarioListChange'})
        #else: 
           #messages.error(request, 'Los datos son incorrectos, vuelve a intentarlo.')
    else:
        form = HorarioSemestralForm(user=request.user)
    return render(request, "calendarapp/form_hora_sem_func_doc.html", context = {"form": form})

# def delFormCalendrioFuncDoc(request, pk):
#     context= {"pk": pk}
#     return render(request, "/eliminar_arcivo.html", context)

def delCalendarioFuncDoc(request, pk):
    if request.method == "POST":
            try:
                record = HorarioSemestral.objects.get(id_horario_semestral=pk)
                record.delete()
                return HttpResponse(status=204, headers={'HX-Trigger': 'calenarioListChange'})
            
            except:
                messages.error(request, 'Ocurrió un error al intentar eliminar el registro.')
                # Eliminar todos los mensajes de error
                storage = messages.get_messages(request)
                for message in storage:
                    if message.level == messages.ERROR:
                        storage.discard(message)
                return render(request, "eliminar_registro.html", context = {"pk": pk})
                
    else:
        
        return render(request, "eliminar_registro.html", context = {"pk": pk})

    #ver como hacer aqui
    #return render(request, "calendarapp/form_hora_sem_func_doc.html")
