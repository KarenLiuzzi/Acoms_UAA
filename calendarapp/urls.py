from django.urls import path
from calendarapp.views.other_views import formCalendarioFuncDoc, obtener_horarios_cita ,EditCalendarioFuncDoc, tipo_cita ,AddCalendarioFuncDoc, delCalendarioFuncDoc, ori_academica, actualizar_campo, TutoriaCreateView, OrientacionAcademicaCreateView, TutoriaUpdateView, OrientacionAcademicaUpdateView, CitaTutoriaDetalle, CitaOrientacionAcademicaDetalle, TutoriaIniciarView#ListCalendarioFuncDoc

from calendarapp.views import CalendarView, CalendarViewNew, AllEventsListView, RunningEventsListView, DetalleCita, CancelarCita
from calendarapp.views.event_list import AprobarCita

app_name = "calendarapp"


urlpatterns = [
    
    path("formulariofundoc/", formCalendarioFuncDoc, name="form_cal_func_doc"),
    # path("listafundoc/", ListCalendarioFuncDoc, name="lista_cal_func_doc"),
    path("formulariofundoc/edit/<int:pk>/", EditCalendarioFuncDoc, name="edit_cal_func_doc"),
    path("formulariofundoc/add/", AddCalendarioFuncDoc, name="add_cal_func_doc"),
    path("formulariofundoc/delete/<int:pk>/", delCalendarioFuncDoc, name="del_cal_func_doc"),
    # path("formfundoc/delete/<int:pk>/", delFormCalendrioFuncDoc, name="delFormCalendrioFuncDoc"),
    
    path("calender/", CalendarViewNew.as_view(), name="calendar"), #este es el calendario
    path("calenders/", CalendarView.as_view(), name="calendars"), #este es el dashboard
    # path("event/new/", views.create_event, name="event_new"),
    # path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    # path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    # path(
    #     "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    # ),
    # path(
    #     "event/<int:pk>/remove",
    #     views.EventMemberDeleteView.as_view(),
    #     name="remove_event",
    # ),
    
    #Citas
    path("tipoCita/", tipo_cita, name="tipo_cita"),
    path('actualizar_campo/', actualizar_campo, name='actualizar_campo'),
    path("detallesCita/<int:id_cita>/", DetalleCita, name="detalles_cita"),
    path("cita/confirmar/<int:id_cita>/", CancelarCita, name="cancelar_cita"),
    path("cita/cancelar/<int:id_cita>/", AprobarCita, name="confirmar_cita"),
    path("tutoria/", TutoriaCreateView.as_view(), name="tuto"),
    path("orientacionAcademica/", OrientacionAcademicaCreateView.as_view(), name="academica"),
    path("modificarCitaTutoria/<int:pk>/", TutoriaUpdateView.as_view(), name="modificar_cita_tutoria"),
    path("modificarCitaOriAcademica/<int:pk>/", OrientacionAcademicaUpdateView.as_view(), name="modificar_cita_ori_academica"),
    path('obtener_horarios_cita/', obtener_horarios_cita),
    path("all-event-list/", AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/<str:tipo_cita>/",RunningEventsListView.as_view(),name="running_events"), 
    path("moredetallesCitaTutoria/<int:pk>/", CitaTutoriaDetalle.as_view() , name="more_detalles_cita_tutoria"),
    path("moredetallesCitaOriAcadem/<int:pk>/", CitaOrientacionAcademicaDetalle.as_view() , name="more_detalles_ori_academica"),
    path("iniciarCitaTutoria/<int:pk>/", TutoriaIniciarView.as_view() , name="iniciar_cita_tutoria"),
]
