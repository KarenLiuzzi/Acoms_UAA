from django.contrib import admin
from accounts.models.user import Persona, TipoDocumento, Alumno, Funcionario, Docente, FuncionarioDocente, User, CarreraAlumno, Facultad, Carrera, Departamento, Materia, MateriaFuncionarioDocente

#registramos nuestros modelos en la pantalla de admin
admin.site.register(Persona)
admin.site.register(TipoDocumento)
admin.site.register(Alumno)
admin.site.register(Funcionario)
admin.site.register(Docente)
admin.site.register(FuncionarioDocente)
admin.site.register(User)

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):

    list_display = ['descripcion_facultad'] # Campos a mostrar en la lista
    list_filter = ('descripcion_facultad',)  # Filtro por campo
    search_fields = ('descripcion_facultad',)  # Búsqueda por campo


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):

    def facultad_nombre(self, obj):
        return '%s' % (obj.id_facultad.descripcion_facultad) 
    facultad_nombre.short_description = 'Facultad'

    list_display = ['descripcion_carrera', 'facultad_nombre'] # Campos a mostrar en la lista
    list_filter = ('descripcion_carrera',)  # Filtro por campo
    search_fields = ('descripcion_carrera',)  # Búsqueda por campo


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):

    def facultad_nombre(self, obj):
        return '%s' % (obj.id_facultad.descripcion_facultad) 
    facultad_nombre.short_description = 'Facultad'

    list_display = ['descripcion_departamento', 'facultad_nombre'] # Campos a mostrar en la lista
    list_filter = ('descripcion_departamento',)  # Filtro por campo
    search_fields = ('descripcion_departamento',)  # Búsqueda por campo


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):

    def departamento_nombre(self, obj):
        return '%s' % (obj.id_departamento.descripcion_departamento) 
    departamento_nombre.short_description = 'Departamento'

    list_display = ['descripcion_materia', 'departamento_nombre'] # Campos a mostrar en la lista
    list_filter = ('descripcion_materia',)  # Filtro por campo
    search_fields = ('descripcion_materia',)  # Búsqueda por campo


@admin.register(MateriaFuncionarioDocente)
class MateriaFuncionarioDocenteAdmin(admin.ModelAdmin):

    def materia_nombre(self, obj):
        return '%s' % (obj.id_materia.descripcion_materia) 
    materia_nombre.short_description = 'Materia'

    def func_doc_nombre(self, obj):
        return '%s' % (obj.id_funcionario_docente) 
    func_doc_nombre.short_description = 'Funcionario/Docente'

    

    list_display = ['func_doc_nombre', 'materia_nombre'] # Campos a mostrar en la lista
    # list_filter = ('descripcion_materia',)  # Filtro por campo
    # search_fields = ('descripcion_materia',)  # Búsqueda por campo


@admin.register(CarreraAlumno)
class CarreraAlumnoAdmin(admin.ModelAdmin):

    def carrera_nombre(self, obj):
        return '%s' % (obj.id_carrera.descripcion_carrera) 
    carrera_nombre.short_description = 'Carrera'

    def func_doc_nombre(self, obj):
        return '%s' % (obj.id_alumno) 
    func_doc_nombre.short_description = 'Alumno'

    

    list_display = ['func_doc_nombre', 'carrera_nombre'] # Campos a mostrar en la lista
    # list_filter = ('descripcion_materia',)  # Filtro por campo
    # search_fields = ('descripcion_materia',)  # Búsqueda por campo