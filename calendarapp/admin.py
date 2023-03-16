from django.contrib import admin
from calendarapp import models
from calendarapp.models.calendario import Dia, Semestre, HorarioSemestral, Convocatoria

#registramos nuestros modelos en la pantalla de admin
admin.site.register(Dia)
admin.site.register(Semestre)
admin.site.register(HorarioSemestral)
admin.site.register(Convocatoria)

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "id",
        "title",
        "user",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]
