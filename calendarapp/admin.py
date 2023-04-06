from django.contrib import admin
from calendarapp import models
from calendarapp.models.calendario import Dia, Semestre, HorarioSemestral, Convocatoria

#registramos nuestros modelos en la pantalla de admin

@admin.register(Dia)
class DiaAdmin(admin.ModelAdmin):
    # def get_model_info(self, obj):
    #     # Obtener todos los campos del modelo
    #     fields = obj._meta.fields
    #     list= [field.name for field in fields]
    #     # Crear una lista con los nombres de los campos
    #     return list
    list_display = ['descripcion_dia'] # Campos a mostrar en la lista
    list_filter = ('descripcion_dia',)  # Filtro por campo
    search_fields = ('descripcion_dia',)  # Búsqueda por campo


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    # def get_model_info(self, obj):
    #     # Obtener todos los campos del modelo
    #     fields = obj._meta.fields
    #     list= [field.name for field in fields]
    #     # Crear una lista con los nombres de los campos
    #     return list
    list_display = ['descripcion_semestre'] # Campos a mostrar en la lista
    list_filter = ('descripcion_semestre',)  # Filtro por campo
    search_fields = ('descripcion_semestre',)  # Búsqueda por campo

@admin.register(HorarioSemestral)
class HorarioSemestralAdmin(admin.ModelAdmin):

    def funcionario_docente_nombre(self, obj):
        return '%s' % (obj.id_funcionario_docente) 
    funcionario_docente_nombre.short_description = 'Funcionario/Docente'

    def convocatoria_nombre(self, obj):
        return '%s %s' % (obj.id_convocatoria.id_semestre.descripcion_semestre, obj.id_convocatoria.anho) 
    convocatoria_nombre.short_description = 'Convocatoria'

    def dia_nombre(self, obj):
        return '%s' % (obj.id_dia.descripcion_dia) 
    dia_nombre.short_description = 'Dia'

    
    list_display = ['funcionario_docente_nombre', 'convocatoria_nombre', 'dia_nombre', 'hora_inicio', 'hora_fin'] # Campos a mostrar en la lista
    list_filter = ["id_funcionario_docente", "id_convocatoria", "hora_inicio", "hora_fin", "id_dia"]  # Filtro por campo
    #search_fields = ["id_funcionario_docente__",] # Búsqueda por campo

@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):

    def convocatoria_nombre(self, obj):
        return '%s %s' % (obj.id_semestre.descripcion_semestre, obj.anho) 
    convocatoria_nombre.short_description = 'Convocatoria'
    
    list_display = ['convocatoria_nombre'] # Campos a mostrar en la lista
    list_filter = ["id_semestre__descripcion_semestre", "anho"]  # Filtro por campo
    search_fields = ["id_semestre__descripcion_semestre", "anho"] # Búsqueda por campo


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
