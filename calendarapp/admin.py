from datetime import datetime
from django.contrib import admin
from django import forms
from calendarapp.models.event import EstadoActividadAcademica,UnidadMedida,EstadoTarea, Parametro, TipoTarea, TipoTutoria, TipoOrientacionAcademica, Motivo 
from calendarapp.models.calendario import Dia, Semestre, Convocatoria
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError

#registramos nuestros modelos en la pantalla de admin

admin.site.register(Permission)
admin.site.site_header= "Administración de AcOms"
admin.site.site_title= "Administración de AcOms"


class TipoOrientacionAcademicaForm(forms.ModelForm):
    class Meta:
        model = TipoOrientacionAcademica
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_tipo_orientacion_academica = cleaned_data.get('descripcion_tipo_orientacion_academica')
        if descripcion_tipo_orientacion_academica is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = TipoOrientacionAcademica.objects.filter(descripcion_tipo_orientacion_academica__contains= descripcion_tipo_orientacion_academica)
            
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
        
class TipoOrientacionAcademicaAdmin(admin.ModelAdmin):
    form = TipoOrientacionAcademicaForm
    
    list_display = ['descripcion_tipo_orientacion_academica'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_orientacion_academica"]  # Filtro por campo
    search_fields = ["descripcion_tipo_orientacion_academica"] # Búsqueda por campo
    
admin.site.register(TipoOrientacionAcademica, TipoOrientacionAcademicaAdmin)


class DiaForm(forms.ModelForm):
    class Meta:
        model = Dia
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_dia = cleaned_data.get('descripcion_dia')
        if descripcion_dia is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = Dia.objects.filter(descripcion_dia__contains= descripcion_dia)
            
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
        
class DiaAdmin(admin.ModelAdmin):
    form= DiaForm
    list_display = ['descripcion_dia'] # Campos a mostrar en la lista
    list_filter = ('descripcion_dia',)  # Filtro por campo
    search_fields = ('descripcion_dia',)  # Búsqueda por campo

admin.site.register(Dia, DiaAdmin)

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_semestre = cleaned_data.get('descripcion_semestre')
        
        if descripcion_semestre is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = Semestre.objects.filter(descripcion_semestre__contains= descripcion_semestre)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
        
class SemestreAdmin(admin.ModelAdmin):
    form= SemestreForm
    list_display = ['descripcion_semestre'] # Campos a mostrar en la lista
    list_filter = ('descripcion_semestre',)  # Filtro por campo
    search_fields = ('descripcion_semestre',)  # Búsqueda por campo

admin.site.register(Semestre, SemestreAdmin)


class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        id_semestre = cleaned_data.get('id_semestre')
        anho = cleaned_data.get('anho')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        # Verificar si ya existe un objeto con la misma descripción
        existing_object = Convocatoria.objects.filter(id_semestre= id_semestre, anho = anho, fecha_inicio= fecha_inicio, fecha_fin= fecha_fin)
        convocatoria= Convocatoria.objects.filter(id_semestre= id_semestre, anho = anho)
        if existing_object.exists():
            raise ValidationError('¡Ya existe un registro con el rango de fechas para el semestre y año!')
        
        if convocatoria.exists():
            raise ValidationError('¡Ya existe un registro para el semestre y año cargado!')

        if ((fecha_inicio and fecha_fin) and (fecha_inicio > fecha_fin)):
            raise ValidationError('¡La fecha inicio no puede ser mayor que la fecha fin!')
        
class ConvocatoriaAdmin(admin.ModelAdmin):
    form= ConvocatoriaForm

    def convocatoria_nombre(self, obj):
        return '%s %s' % (obj.id_semestre.descripcion_semestre, obj.anho) 
    convocatoria_nombre.short_description = 'Convocatoria'
    
    list_display = ['convocatoria_nombre'] # Campos a mostrar en la lista
    list_filter = ["id_semestre__descripcion_semestre", "anho"]  # Filtro por campo
    search_fields = ["id_semestre__descripcion_semestre", "anho"] # Búsqueda por campo
    
admin.site.register(Convocatoria, ConvocatoriaAdmin)

class EstadoActividadAcademicaForm(forms.ModelForm):
    class Meta:
        model = EstadoActividadAcademica
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_estado_actividad_academica = cleaned_data.get('descripcion_estado_actividad_academica')
        
        if descripcion_estado_actividad_academica is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = EstadoActividadAcademica.objects.filter(descripcion_estado_actividad_academica__contains= descripcion_estado_actividad_academica)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')

class EstadoActividadAcademicaAdmin(admin.ModelAdmin):
    form= EstadoActividadAcademicaForm
    list_display = ['descripcion_estado_actividad_academica'] # Campos a mostrar en la lista
    list_filter = ["descripcion_estado_actividad_academica"]  # Filtro por campo
    search_fields = ["descripcion_estado_actividad_academica"] # Búsqueda por campo
    
admin.site.register(EstadoActividadAcademica, EstadoActividadAcademicaAdmin)


class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_unidad_medida = cleaned_data.get('descripcion_unidad_medida')
        
        if descripcion_unidad_medida is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = UnidadMedida.objects.filter(descripcion_unidad_medida__contains= descripcion_unidad_medida)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')

class UnidadMedidaAdmin(admin.ModelAdmin):
    form= UnidadMedidaForm
    
    list_display = ['descripcion_unidad_medida'] # Campos a mostrar en la lista
    list_filter = ["descripcion_unidad_medida"]  # Filtro por campo
    search_fields = ["descripcion_unidad_medida"] # Búsqueda por campo

admin.site.register(UnidadMedida, UnidadMedidaAdmin)


class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        id_unidad_medida = cleaned_data.get('id_unidad_medida')
        descripcion_parametro = cleaned_data.get('descripcion_parametro')
        valor = cleaned_data.get('valor')
        es_orientacion_academica = cleaned_data.get('es_orientacion_academica')
        es_tutoria = cleaned_data.get('es_tutoria')

        if valor is not None:
            if valor <= 0:
                raise ValidationError('¡El valor debe ser mayor que cero!')
        
        if (es_orientacion_academica == True and es_tutoria == True):
            raise ValidationError('¡Por favor, selecciona solo un campo de tipo de actividad académica, no ambos!')
        
        if (es_orientacion_academica == False and es_tutoria == False):
            raise ValidationError('¡Por favor, selecciona una actividad academica académica!')
        
        if es_orientacion_academica == True:
            # Verificar si ya existe un objeto con la misma descripción
            ins_es_orientacion_academica = Parametro.objects.filter(es_orientacion_academica= es_orientacion_academica)
        
            if ins_es_orientacion_academica.exists():
                raise ValidationError('¡Ya existe un registro cargado para orientación académica en la base de datos!')
                    
        if es_tutoria == True:
            # Verificar si ya existe un objeto con la misma descripción
            ins_es_tutoria = Parametro.objects.filter(es_tutoria= es_tutoria)
        
            if ins_es_tutoria.exists():
                raise ValidationError('¡Ya existe un registro cargado para tutoría en la base de datos!')
class ParametroAdmin(admin.ModelAdmin):

    form= ParametroForm
    def unidad_medida_nombre(self, obj):
        return '%s' % (obj.id_unidad_medida.descripcion_unidad_medida) 
    unidad_medida_nombre.short_description = 'Unidad Medida'
    
    list_display = ['unidad_medida_nombre', 'valor', 'es_orientacion_academica', 'es_tutoria'] # Campos a mostrar en la lista
    # list_filter = ["unidad_medida_nombre"]  # Filtro por campo
    # search_fields = ["unidad_medida_nombre"] # Búsqueda por campo


admin.site.register(Parametro, ParametroAdmin)
class TipoTutoriaForm(forms.ModelForm):
    class Meta:
        model = TipoTutoria
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_tipo_tutoria = cleaned_data.get('descripcion_tipo_tutoria')
        
        if descripcion_tipo_tutoria is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = TipoTutoria.objects.filter(descripcion_tipo_tutoria__contains= descripcion_tipo_tutoria)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
            

class TipoTutoriaAdmin(admin.ModelAdmin):
    form= TipoTutoriaForm
    
    list_display = ['descripcion_tipo_tutoria'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_tutoria"]  # Filtro por campo
    search_fields = ["descripcion_tipo_tutoria"] # Búsqueda por campo

admin.site.register(TipoTutoria, TipoTutoriaAdmin)

class MotivoForm(forms.ModelForm):
    class Meta:
        model = Motivo
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_motivo = cleaned_data.get('descripcion_motivo')
        id_tipo_orientacion_academica= cleaned_data.get('id_tipo_orientacion_academica')
        if descripcion_motivo is not None and id_tipo_orientacion_academica is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = Motivo.objects.filter(descripcion_motivo__contains= descripcion_motivo, id_tipo_orientacion_academica= id_tipo_orientacion_academica)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos para el tipo de orientación académica!')
            
class MotivoAdmin(admin.ModelAdmin):

    form=  MotivoForm
    def tipo_nombre(self, obj):
        return '%s' % (obj.id_tipo_orientacion_academica.descripcion_tipo_orientacion_academica) 
    tipo_nombre.short_description = 'Tipo Orientacion Academica'
    
    list_display = ['tipo_nombre', 'descripcion_motivo'] # Campos a mostrar en la lista
    list_filter = ["descripcion_motivo"]  # Filtro por campo
    search_fields = ["descripcion_motivo"] # Búsqueda por campo

admin.site.register(Motivo, MotivoAdmin)

class TipoTareaForm(forms.ModelForm):
    class Meta:
        model = TipoTarea
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_tipo_tarea = cleaned_data.get('descripcion_tipo_tarea')
        
        if descripcion_tipo_tarea is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = TipoTarea.objects.filter(descripcion_tipo_tarea__contains= descripcion_tipo_tarea)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
            
class TipoTareaAdmin(admin.ModelAdmin):
    form= TipoTareaForm
    
    list_display = ['descripcion_tipo_tarea'] # Campos a mostrar en la lista
    list_filter = ["descripcion_tipo_tarea"]  # Filtro por campo
    search_fields = ["descripcion_tipo_tarea"] # Búsqueda por campo
    
admin.site.register(TipoTarea, TipoTareaAdmin)

class EstadoTareaForm(forms.ModelForm):
    class Meta:
        model = EstadoTarea
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion_estado_tarea = cleaned_data.get('descripcion_estado_tarea')
        
        if descripcion_estado_tarea is not None:
            # Verificar si ya existe un objeto con la misma descripción
            existing_object = EstadoTarea.objects.filter(descripcion_estado_tarea__contains= descripcion_estado_tarea)
        
            if existing_object.exists():
                raise ValidationError('¡La descripción ya existe en la base de datos!')
class EstadoTareaAdmin(admin.ModelAdmin):

    form= EstadoTareaForm
    list_display = ['descripcion_estado_tarea'] # Campos a mostrar en la lista
    list_filter = ["descripcion_estado_tarea"]  # Filtro por campo
    search_fields = ["descripcion_estado_tarea"] # Búsqueda por campo

admin.site.register(EstadoTarea, EstadoTareaAdmin)