from django.urls import path
from notify.views import NotificationList, actualizar_notificacion_leida

app_name = "notify"

urlpatterns = [
    path("notificacion/", NotificationList.as_view(), name="notificaciones"),
    path("actualizarNotify/", actualizar_notificacion_leida, name="actualizar_notificacion"),
]
