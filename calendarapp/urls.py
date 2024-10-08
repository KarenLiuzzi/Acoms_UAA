from django.urls import path
from calendarapp.views.other_views import TutoriaCreateView, formCalendarioFuncDoc, obtener_horarios_cita ,EditCalendarioFuncDoc, tipo_cita, tipo_acti_academ, AddCalendarioFuncDoc, delCalendarioFuncDoc, ori_academica, actualizar_campo, CitaTutoriaCreateView, CitaOrientacionAcademicaCreateView, CitaTutoriaUpdateView, CitaOrientacionAcademicaUpdateView, CitaTutoriaDetalle, CitaOrientacionAcademicaDetalle, CitaTutoriaIniciarView, CitaOrientacionAcademicaIniciarView, OrientacionAcademicaCreateView, TutoriaDetalle, OrientacionAcademicaDetalle, TutoriaUpdateView, TareasView, OrientacionAcademicaUpdateView, AddTarea#ListCalendarioFuncDoc

from calendarapp.views import CalendarView, CalendarViewNew, AllEventsListView, RunningEventsListView, DetalleCita, CancelarCita
from calendarapp.views.event_list import AprobarCita, ActividadesAcademicasListView, RunningActividadesAcademicasListView, DetalleActividadesAcademicas, CancelarActividadAcademica, FinalizarActividadAcademica, CancelarTarea, IniciarTarea, FinalizarTarea, About, RechazarCita
from calendarapp.views.reportes import ReporteTutoriaView, actualizar_campos_reportes, ReporteOrientacionAcademicaView, ReporteCitasView, ReporteTareasView
app_name = "calendarapp"


urlpatterns = [
    
    path("formulariofundoc/", formCalendarioFuncDoc, name="form_cal_func_doc"),
    path("formulariofundoc/edit/<int:pk>/", EditCalendarioFuncDoc, name="edit_cal_func_doc"),
    path("formulariofundoc/add/", AddCalendarioFuncDoc, name="add_cal_func_doc"),
    path("formulariofundoc/delete/<int:pk>/", delCalendarioFuncDoc, name="del_cal_func_doc"),
    path("calender/", CalendarViewNew.as_view(), name="calendar"), #este es el calendario
    path("calenders/", CalendarView.as_view(), name="calendars"), #este es el dashboard
    
    #Citas
    path("tipoCita/", tipo_cita, name="tipo_cita"),
    path('actualizar_campo/', actualizar_campo, name='actualizar_campo'),
    path("detallesCita/<int:id_cita>/", DetalleCita, name="detalles_cita"),
    path("cita/confirmar/<int:id_cita>/", AprobarCita, name="confirmar_cita"),
    path("cita/cancelar/<int:id_cita>/", CancelarCita, name="cancelar_cita"),
    path("cita/rechazar/<int:id_cita>/", RechazarCita, name="rechazar_cita"),
    path("tutoria/", CitaTutoriaCreateView.as_view(), name="tuto"),
    path("orientacionAcademica/", CitaOrientacionAcademicaCreateView.as_view(), name="academica"),
    path("modificarCitaTutoria/<int:pk>/", CitaTutoriaUpdateView.as_view(), name="modificar_cita_tutoria"),
    path("modificarCitaOriAcademica/<int:pk>/", CitaOrientacionAcademicaUpdateView.as_view(), name="modificar_cita_ori_academica"),
    path('obtener_horarios_cita/', obtener_horarios_cita),
    path("all-event-list/", AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/<str:tipo_cita>/",RunningEventsListView.as_view(),name="running_events"), 
    path("moredetallesCitaTutoria/<int:pk>/", CitaTutoriaDetalle.as_view() , name="more_detalles_cita_tutoria"),
    path("moredetallesCitaOriAcadem/<int:pk>/", CitaOrientacionAcademicaDetalle.as_view() , name="more_cita_detalles_ori_academica"),
    path("iniciarCitaTutoria/<int:pk>/", CitaTutoriaIniciarView.as_view() , name="iniciar_cita_tutoria"),
    path("iniciarCitaOrientacionAcademica/<int:pk>/", CitaOrientacionAcademicaIniciarView.as_view() , name="iniciar_cita_ori_academ"),
    
    
    
    
    #Actividades Academicas
    path("tipoActiAcadem/", tipo_acti_academ, name="tipo_acti_academ"),
    path("all-acti_academ-list/", ActividadesAcademicasListView.as_view(), name="all_acti_academ"),
    path("running-acti_academ-list/<str:tipo_cita>/",RunningActividadesAcademicasListView.as_view(),name="running_acti_academ"), 
    path("actiAcademTutoria/", TutoriaCreateView.as_view(), name="acti_academ_tutoria"),
    path("actiAcademOrientacion/", OrientacionAcademicaCreateView.as_view(), name="acti_academ_orientacion"),
    path("detallesActiAcademicas/<int:id_tutoria>/<int:id_ori_academ>/", DetalleActividadesAcademicas, name="detalles_acti_academ"),
    path("moredetallesTutoria/<int:pk>/", TutoriaDetalle.as_view() , name="more_detalles_tutoria"),
    path("moredetallesOrientacionAcademica/<int:pk>/", OrientacionAcademicaDetalle.as_view() , name="more_detalles_ori_academica"),
    path("actividad_academica/cancelar/<int:id_tutoria>/<int:id_ori_academ>/", CancelarActividadAcademica, name="cancelar_actividad_academica"),
    path("actividad_academica/finalizar/<int:id_tutoria>/<int:id_ori_academ>/", FinalizarActividadAcademica, name="finalizar_actividad_academica"),
    path("modificarTutoria/<int:pk>/", TutoriaUpdateView.as_view(), name="modificar_tutoria"),
    path("modificarOrientacion/<int:pk>/", OrientacionAcademicaUpdateView.as_view(), name="modificar_orientacion"),
    
    #Tareas
    path("tareas/", TareasView.as_view(), name="tareas"),
    path("tarea/finalizar/<int:id_tarea>/", FinalizarTarea, name="finalizar_tarea"),
    path("tarea/iniciar/<int:id_tarea>/", IniciarTarea, name="iniciar_tarea"),
    path("tarea/cancelar/<int:id_tarea>/", CancelarTarea, name="cancelar_tarea"),
    path("nuevaTarea/", AddTarea, name="nueva_tarea"),
    
    
    #adicionales
    path("about/", About, name="about"),
    
    
    #reportes
    path("reporte/tutoria/", ReporteTutoriaView.as_view(), name="reporte_tutoria"),
    path("reporte/cita/", ReporteCitasView.as_view(), name="reporte_cita"),
    path("reporte/orientacion/", ReporteOrientacionAcademicaView.as_view(), name="reporte_orientacion"),
    path("reporte/tarea/", ReporteTareasView.as_view(), name="reporte_tarea"),
    path('actualizar_campos_reportes/', actualizar_campos_reportes, name='actualizar_campos_reportes'),
    
    
    
    
]
