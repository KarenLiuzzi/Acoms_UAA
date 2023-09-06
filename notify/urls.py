from django.urls import path
from notify.views import NotificationList

app_name = "notify"

urlpatterns = [
    path("notificacion/", NotificationList.as_view(), name="notificaciones"),
]
