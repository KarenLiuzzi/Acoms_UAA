from django.contrib import admin
from calendarapp import models
from calendarapp.models.event import EstadoActividadAcademica, UnidadMedida, EstadoTarea, Parametro, TipoTarea, TipoTutoria, TipoOrientacionAcademica, Motivo
from calendarapp.models.calendario import Dia, Semestre, HorarioSemestral, Convocatoria

#registramos nuestros modelos en la pantalla de admin

@admin.register(Dia)
class DiaAdmin(admin.ModelAdmin):

    list_display = ['descripcion_dia'] # Campos a mostrar en la lista
    list_filter = ('descripcion_dia',)  # Filtro por campo
    search_fields = ('descripcion_dia',)  # Búsqueda por campo


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):

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

@admin.register(EstadoActividadAcademica)
class EstadoActividadAcademicaAdmin(admin.ModelAdmin):
    
    list_display = ['descripcion_estado_actividad_academica'] # Campos a mostrar en la lista
    list_filter = ["descripcion_estado_actividad_academica"]  # Filtro por campo
    search_fields = ["descripcion_estado_actividad_academica"] # Búsqueda por campo

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_unidad_medida'] # Campos a mostrar en la lista
    list_filter = ["descripcion_unidad_medida"]  # Filtro por campo
    search_fields = ["descripcion_unidad_medida"] # Búsqueda por campo

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):

    def unidad_medida_nombre(self, obj):
        return '%s' % (obj.id_unidad_medida.descripcion_unidad_medida) 
    unidad_medida_nombre.short_description = 'Unidad Medida'
    
    list_display = ['unidad_medida_nombre', 'valor', 'es_orientacion_academica', 'es_tutoria'] # Campos a mostrar en la lista
    # list_filter = ["unidad_medida_nombre"]  # Filtro por campo
    # search_fields = ["unidad_medida_nombre"] # Búsqueda por campo

@admin.register(TipoTutoria)
class TipoTutoriaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_tipo_tutoria'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_tutoria"]  # Filtro por campo
    search_fields = ["descripcion_tipo_tutoria"] # Búsqueda por campo


@admin.register(TipoOrientacionAcademica)
class TipoOrientacionAcademicaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_tipo_orientacion_academica'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_orientacion_academica"]  # Filtro por campo
    search_fields = ["descripcion_tipo_orientacion_academica"] # Búsqueda por campo


@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_motivo'] # Campos a mostrar en la lista
    list_filter = ["descripcion_motivo"]  # Filtro por campo
    search_fields = ["descripcion_motivo"] # Búsqueda por campo


@admin.register(TipoTarea)
class TipoTareaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_tipo_tarea'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_tarea"]  # Filtro por campo
    search_fields = ["descripcion_tipo_tarea"] # Búsqueda por campo

@admin.register(EstadoTarea)
class EstadoTareaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_estado_tarea'] # Campos a mostrar en la lista
    list_filter = ["descripcion_estado_tarea"]  # Filtro por campo
    search_fields = ["descripcion_estado_tarea"] # Búsqueda por campo


# @admin.register(models.Event)
# class EventAdmin(admin.ModelAdmin):
#     model = models.Event
#     list_display = [
#         "observacion",
#         "datetime_inicio_estimado",
#         "datetime_fin_estimado",
#     ]
#     list_filter = ["datetime_inicio_estimado", "datetime_fin_estimado"]
#     search_fields = ["observacion"]


# @admin.register(models.EventMember)
# class EventMemberAdmin(admin.ModelAdmin):
#     model = models.EventMember
#     list_display = ["id", "event", "user", "created_at", "updated_at"]
#     list_filter = ["event"]
