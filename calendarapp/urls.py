from django.urls import path
from calendarapp.views.other_views import formCalendarioFuncDoc, EditCalendarioFuncDoc, tipo_cita ,AddCalendarioFuncDoc, delCalendarioFuncDoc, tutoria, ori_academica #ListCalendarioFuncDoc

from . import views

app_name = "calendarapp"


urlpatterns = [
    
    path("formulariofundoc/", formCalendarioFuncDoc, name="form_cal_func_doc"),
    # path("listafundoc/", ListCalendarioFuncDoc, name="lista_cal_func_doc"),
    path("formulariofundoc/edit/<int:pk>/", EditCalendarioFuncDoc, name="edit_cal_func_doc"),
    path("formulariofundoc/add/", AddCalendarioFuncDoc, name="add_cal_func_doc"),
    path("formulariofundoc/delete/<int:pk>/", delCalendarioFuncDoc, name="del_cal_func_doc"),
    # path("formfundoc/delete/<int:pk>/", delFormCalendrioFuncDoc, name="delFormCalendrioFuncDoc"),
    
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path(
        "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
    
    
    
    #AGREGADOS DE PRUEBA
    path("tutoria/", tutoria, name="tuto"),
    path("orientacionAcademica/", ori_academica, name="academica"),
    path("tipoCita/", tipo_cita, name="tipo_cita"),
]
