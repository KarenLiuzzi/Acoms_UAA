from django.contrib import admin
from calendarapp import models
from calendarapp.models.event import EstadoActividadAcademica, Event,UnidadMedida,Tutoria , OrientacionAcademica , Cita,EstadoTarea, Parametro, TipoTarea, TipoTutoria, TipoOrientacionAcademica, Motivo #,DetalleActividadAcademica
from calendarapp.models.calendario import Dia, Semestre, HorarioSemestral, Convocatoria
from django.contrib.auth.models import Permission

#registramos nuestros modelos en la pantalla de admin

admin.site.register(Permission)


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
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    def estado_acti_nombre(self, obj):
        return '%s' % (obj.id_estado_actividad_academica.descripcion_estado_actividad_academica) 
    estado_acti_nombre.short_description = 'Estado'
    
    def convocatoria_nombre(self, obj):
        return '%s %s' % (obj.id_convocatoria.id_semestre.descripcion_semestre, obj.id_convocatoria.anho) 
    convocatoria_nombre.short_description = 'Convocatoria'
    
    def facultad_nombre(self, obj):
        return '%s' % (obj.id_facultad.descripcion_facultad) 
    facultad_nombre.short_description = 'Facultad'
    
    def materia_nombre(self, obj):
        #si no existe el objeto, entonces devuelve vacio o None
        try:
            return '%s' % (obj.id_facultad.descripcion_facultad)
        except AttributeError:
            return ''
    
    def departamento_nombre(self, obj):
        return '%s' % (obj.id_departamento.descripcion_departamento) 
    departamento_nombre.short_description = 'Departamento'
    
    def encargado_nombre(self, obj):
        return '%s %s' % (obj.id_funcionario_docente_encargado.id_funcionario_docente.nombre, obj.id_funcionario_docente_encargado.id_funcionario_docente.apellido) 
    encargado_nombre.short_description = 'Encargado'
    
    def receptor_nombre(self, obj):
        #si no existe el objeto, entonces devuelve vacio o None
        try:
            return '%s %s' % (obj.id_persona_receptor.nombre, obj.id_persona_receptor.apellido) 
        except AttributeError:
            return ''
    
    
    def alta_nombre(self, obj):
        return '%s %s' % (obj.id_persona_alta.nombre, obj.id_persona_alta.apellido) 
    alta_nombre.short_description = 'Usuario alta'
    
    
    list_display = ['estado_acti_nombre', 'convocatoria_nombre','facultad_nombre' ,'materia_nombre' ,'receptor_nombre','departamento_nombre', 'encargado_nombre' , 'alta_nombre' , 'datetime_inicio_estimado', 'datetime_fin_estimado', 'datetime_inicio_real', 'datetime_fin_real', 'datetime_registro', 'observacion', 'nro_curso'] # Campos a mostrar en la lista
    #list_filter = ["descripcion_estado_tarea"]  # Filtro por campo
    #search_fields = ["descripcion_estado_tarea"] # Búsqueda por campo



@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    
    def Parametro_nombre(self, obj):
        return '%s %s' % (obj.id_parametro.descripcion_parametro, obj.id_parametro.valor) 
    Parametro_nombre.short_description = 'Parametro'
    
    list_display = ['Parametro_nombre', 'es_tutoria','es_orientacion_academica' , 'es_notificable', 'motivo'] # Campos a mostrar en la lista



@admin.register(OrientacionAcademica)
class OrientacionAcademicaAdmin(admin.ModelAdmin):
    
    def motivo_nombre(self, obj):
        return '%s' % (obj.id_motivo.descripcion_motivo) 
    motivo_nombre.short_description = 'Motivo'
    
    
    def tipo_nombre(self, obj):
        return '%s' % (obj.id_tipo_orientacion_academica.descripcion_tipo_orientacion_academica) 
    tipo_nombre.short_description = 'Tipo'
    
    
    list_display = ['id_cita', 'motivo_nombre','tipo_nombre'] # Campos a mostrar en la lista

#comentamos momentaneamente
# @admin.register(DetalleActividadAcademica)
# class DetalleActividadAcademicaAdmin(admin.ModelAdmin):
    
#     def participante_nombre(self, obj):
#         return '%s %s' % (obj.id_participante.nombre, obj.id_participante.apellido) 
#     participante_nombre.short_description = 'Participante'
    
#     list_display = ['id_actividad_academica', 'participante_nombre', 'es_docente', 'es_funcionario', 'es_alumno'] # Campos a mostrar en la lista


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


