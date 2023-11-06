from django.contrib import admin
from calendarapp.models.event import EstadoActividadAcademica,UnidadMedida,EstadoTarea, Parametro, TipoTarea, TipoTutoria, TipoOrientacionAcademica, Motivo 
from calendarapp.models.calendario import Dia, Semestre, Convocatoria
from django.contrib.auth.models import Permission

#registramos nuestros modelos en la pantalla de admin

admin.site.register(Permission)
admin.site.site_header= "Administración de AcOms"
admin.site.site_title= "Administración de AcOms"

@admin.register(TipoOrientacionAcademica)
class TipoOrientacionAcademicaAdmin(admin.ModelAdmin):

    
    list_display = ['descripcion_tipo_orientacion_academica'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_orientacion_academica"]  # Filtro por campo
    search_fields = ["descripcion_tipo_orientacion_academica"] # Búsqueda por campo

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

@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):

    def tipo_nombre(self, obj):
        return '%s' % (obj.id_tipo_orientacion_academica.descripcion_tipo_orientacion_academica) 
    tipo_nombre.short_description = 'Tipo Orientacion Academica'
    
    list_display = ['tipo_nombre', 'descripcion_motivo'] # Campos a mostrar en la lista
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