from django import forms
from django.contrib import admin
from accounts.models.user import User, Persona, TipoDocumento, Alumno, CarreraAlumno, MateriaCarrera, Funcionario, Docente, FuncionarioDocente, User, Facultad, Carrera, Departamento, Materia #, MateriaFuncionarioDocente , CarreraAlumno
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

#registramos nuestros modelos en la pantalla de admin
#admin.site.register(Persona)
# admin.site.register(TipoDocumento)
#admin.site.register(Alumno)
#admin.site.register(Funcionario)
#admin.site.register(Docente)
# admin.site.register(FuncionarioDocente)
# admin.site.register(User)

class FuncionarioDocenteForm(forms.ModelForm):
    class Meta:
        model = FuncionarioDocente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionarioDocenteForm, self).__init__(*args, **kwargs)
        # Modificamos las propiedades del campo id_departamento y id_facultad según tus requisitos
        self.fields['id_departamento'].required = False
        self.fields['id_facultad'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        id_departamento = cleaned_data.get('id_departamento')
        id_facultad = cleaned_data.get('id_facultad')

        if id_departamento and id_facultad:
            raise ValidationError('¡Por favor, selecciona solo un departamento o una facultad, no ambos!')
        
        if id_departamento is None and id_facultad is None:
            raise ValidationError('¡Por favor, selecciona un departamento o una facultad, no ambos!')
        
class FuncionarioDocenteAdmin(admin.ModelAdmin):
    form = FuncionarioDocenteForm

admin.site.register(FuncionarioDocente, FuncionarioDocenteAdmin)
   
class UserFormCreate(forms.ModelForm):
    # Personaliza el formulario de creación de usuarios
    documento = forms.CharField(
        label="documento",
        widget=forms.TextInput(attrs={"class": "form-control"}), error_messages= {'required': 'Por favor ingrese su Nro de Documento'}, strip= True
    )
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    
    id_persona = forms.CharField(
        label="id_persona",
        widget=forms.TextInput(attrs={"class": "hidden"}),
        disabled= True, required= False,
    )

    class Meta:
        model = User
        fields = ('documento', 'email', 'password', 'is_staff', 'is_active', 'groups','is_superuser', 'id_persona', 'groups', 'materia_func_doc')

    def clean_id_persona(self):
        doc = self.cleaned_data.get("documento")
        per = Persona.objects.filter(documento=doc).first()
        # if per is not None:
        if per is not None:
            #dict = model_to_dict(per.first())
            id_persona = per
            #print("paso asignacion persona")

        else:
            raise ValidationError("No existe una persona con el Nro de documento en la Base de Datos!")
        return id_persona
    
    def clean_documento(self):
        doc = self.cleaned_data.get("documento")
        nro_doc=  Persona.objects.filter(documento= doc)
        user_doc = User.objects.filter(documento= doc)
        #validamos si existe una persona con el nro de docuento en nuestra base de datos
        if nro_doc.count() == 0:
            raise ValidationError("El nro de documento no existe en la base de Datos!")
        #Validamos si existe un usuario con el nro de documento
        if user_doc.count() != 0:
            raise ValidationError("Ya existe un usuario con el Nro de Cédula!")
        return doc
 
    
    def save(self, commit=True):
        # Sobrescribimos el valor de la persona
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        doc = self.cleaned_data.get("documento")
        per = Persona.objects.filter(documento=doc).first()
        print(per)
        if per:
            user.id_persona = per  # Modificar el valor del campo
        else:
            raise ValidationError("No existe la persona con el nro de cedula!")
        if commit:
            user.save()
        return user
    
class UserFormModify(forms.ModelForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = User
        fields = ('documento', 'email', 'is_staff', 'is_active', 'groups', 'materia_func_doc')
    

class UserAdmin(admin.ModelAdmin):
        
    forms= UserFormModify
    fields =  ['email', 'is_staff', 'is_active', 'is_superuser', 'groups', 'materia_func_doc']  # Agrega los campos que deseas mostrar en el formulario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_staff', 'is_active', 'is_superuser', 'groups', 'materia_func_doc'),
        }),
    )
    filter_vertical= ('groups', 'materia_func_doc',)
    search_fields = ['email']
    
    def has_add_permission(self, request):
        return False
    
admin.site.register(User, UserAdmin)



#***************************************ESTOS*************************
# @admin.register(Facultad)
# class FacultadAdmin(admin.ModelAdmin):

#     list_display = ['descripcion_facultad'] # Campos a mostrar en la lista
#     list_filter = ('descripcion_facultad',)  # Filtro por campo
#     search_fields = ('descripcion_facultad',)  # Búsqueda por campo


# @admin.register(Carrera)
# class CarreraAdmin(admin.ModelAdmin):

#     def facultad_nombre(self, obj):
#         return '%s' % (obj.id_facultad.descripcion_facultad) 
#     facultad_nombre.short_description = 'Facultad'

#     list_display = ['descripcion_carrera', 'facultad_nombre'] # Campos a mostrar en la lista
#     list_filter = ('descripcion_carrera',)  # Filtro por campo
#     search_fields = ('descripcion_carrera',)  # Búsqueda por campo


# @admin.register(Departamento)
# class DepartamentoAdmin(admin.ModelAdmin):

#     def facultad_nombre(self, obj):
#         return '%s' % (obj.id_facultad.descripcion_facultad) 
#     facultad_nombre.short_description = 'Facultad'

#     list_display = ['descripcion_departamento', 'facultad_nombre'] # Campos a mostrar en la lista
#     list_filter = ('descripcion_departamento',)  # Filtro por campo
#     search_fields = ('descripcion_departamento',)  # Búsqueda por campo


# @admin.register(Materia)
# class MateriaAdmin(admin.ModelAdmin):

#     def departamento_nombre(self, obj):
#         return '%s' % (obj.id_departamento.descripcion_departamento) 
#     departamento_nombre.short_description = 'Departamento'

#     list_display = ['descripcion_materia', 'departamento_nombre'] # Campos a mostrar en la lista
#     list_filter = ('descripcion_materia',)  # Filtro por campo
#     search_fields = ('descripcion_materia',)  # Búsqueda por campo




# # #esto tb comentamos momentaneamente
# @admin.register(CarreraAlumno)
# class CarreraAlumnoAdmin(admin.ModelAdmin):

#     def carrera_nombre(self, obj):
#         return '%s' % (obj.id_carrera.descripcion_carrera) 
#     carrera_nombre.short_description = 'Carrera'

#     def func_doc_nombre(self, obj):
#         return '%s' % (obj.id_alumno) 
#     func_doc_nombre.short_description = 'Alumno'

    

#     list_display = ['func_doc_nombre', 'carrera_nombre'] # Campos a mostrar en la lista
#     # list_filter = ('descripcion_materia',)  # Filtro por campo
#     # search_fields = ('descripcion_materia',)  # Búsqueda por campo


# # from accounts.models.user import Post
# # admin.site.register(Post) 



# @admin.register(MateriaCarrera)
# class MateriaCarreraAdmin(admin.ModelAdmin):

#     def carrera_nombre(self, obj):
#         return '%s' % (obj.id_carrera.descripcion_carrera) 
#     carrera_nombre.short_description = 'Carrera'

#     def materia_nombre(self, obj):
#         return '%s' % (obj.id_materia.descripcion_materia) 
#     materia_nombre.short_description = 'Materia'


#     list_display = ['materia_nombre', 'carrera_nombre']
    
#esto tb comentamos momentaneamente
# @admin.register(MateriaFuncionarioDocente)
# class MateriaFuncionarioDocenteAdmin(admin.ModelAdmin):

#     def materia_nombre(self, obj):
#         return '%s' % (obj.id_materia.descripcion_materia) 
#     materia_nombre.short_description = 'Materia'

#     def func_doc_nombre(self, obj):
#         return '%s' % (obj.id_funcionario_docente) 
#     func_doc_nombre.short_description = 'Funcionario/Docente'

    

#     list_display = ['func_doc_nombre', 'materia_nombre'] # Campos a mostrar en la lista
#     # list_filter = ('descripcion_materia',)  # Filtro por campo
#     # search_fields = ('descripcion_materia',)  # Búsqueda por campo
