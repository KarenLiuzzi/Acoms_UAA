from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from calendarapp.models.event import Cita, Tutoria, OrientacionAcademica
from accounts.models.user import Persona, FuncionarioDocente
from calendarapp.models import Event
from django.forms.models import model_to_dict
from itertools import chain

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
        
        #devolvemos solo aquellos registros que correspondan al usuario logeado
        if current_user.has_perm('calendarapp.iniciar_cita'):
            ins_funcionario_docente= FuncionarioDocente.objects.get(id_funcionario_docente= ins_persona)
            #actividades con citas
            citas = Cita.objects.select_related("id_cita").filter(id_cita__id_funcionario_docente_encargado= ins_funcionario_docente)
            #tutorias sin citas
            tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_funcionario_docente_encargado= ins_funcionario_docente)
            #orientaciones sin citas
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_funcionario_docente_encargado= ins_funcionario_docente)
            # Combinar los dos querysets en una sola variable
            running_events= list(chain(citas, tutorias, orientaciones))
        else:
             #actividades con citas
            citas = Cita.objects.select_related("id_cita").filter(id_cita__id_persona_alta= ins_persona)
            #tutorias sin citas
            tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None, id_tutoria__id_persona_alta= ins_persona)
            #orientaciones sin citas
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None, id_orientacion_academica__id_persona_alta= ins_persona)
            # Combinar los dos querysets en una sola variable
            running_events= list(chain(citas, tutorias, orientaciones))
            
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
