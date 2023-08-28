from time import strptime
from django.forms import ModelForm, DateInput, TimeInput, ValidationError, Form
from requests import request
from calendarapp.models import Event, EventMember
from calendarapp.models.event import Parametro, EstadoActividadAcademica, Cita, DetalleActividadAcademica
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from accounts.models.user import FuncionarioDocente, Facultad, Materia, Departamento, Persona
from django import forms


""" esto es un ejemplo de como se veria el metodo
fecha1 = '2023-04-24 10:00:00'
fecha2 = '2023-04-24 11:30:00'
minutos = 15

divisiones = dividir_fechas_en_minutos(fecha1, fecha2, minutos)
for fecha_hora in divisiones:
    print(fecha_hora.strftime('%Y-%m-%d %H:%M:%S'))
    
resultado:
2023-04-24 10:15:00
2023-04-24 10:30:00
2023-04-24 10:45:00
2023-04-24 11:00:00
2023-04-24 11:15:00
2023-04-24 11:30:00

"""


"""
evento
id_estado_actividad_academica= models.ForeignKey(EstadoActividadAcademica, on_delete=models.PROTECT, related_name='estado_acti_aca')
    id_convocatoria= models.ForeignKey(Convocatoria, on_delete=models.PROTECT, related_name='convocatoria')
    id_facultad= models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name='facultad')
    id_materia= models.ForeignKey(Materia, on_delete=models.PROTECT, related_name='materia', null= True)
    id_departamento= models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='departamento')
    id_funcionario_docente_encargado= models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, related_name='funcionario_docente_encarcado')
    id_persona_receptor= models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='persona_receptor')
    id_persona_alta= models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='persona_alta')
    datetime_inicio_estimado = models.DateTimeField()
    datetime_fin_estimado = models.DateTimeField()
    datetime_inicio_real = models.DateTimeField(null= True, default= None)
    datetime_fin_real = models.DateTimeField(null= True, default= None)
    datetime_registro = models.DateTimeField(auto_now=True)
    observacion= models.CharField(max_length=500, null= True)
    nro_curso= models.CharField(max_length=30, null= True)"""

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["observacion", "datetime_inicio_estimado", "datetime_fin_estimado"]
        # datetime-local is a HTML5 input type
        widgets = {
            #"title": forms.TextInput(
            #   attrs={"class": "form-control", "placeholder": "Enter event title"}
            #),
            "observacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Observación",
                }
            ),
            "datetime_inicio_estimado": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "datetime_fin_estimado": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        #exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["datetime_inicio_estimado"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["datetime_fin_estimado"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]

# En resumen, la principal diferencia entre "forms.ModelForm" y "ModelForm" es que "forms.ModelForm" es una clase que 
# ofrece algunas funcionalidades adicionales para personalizar la representación y validación de los campos del formulario,
# mientras que "ModelForm" es una clase más simple que se utiliza para crear formularios basados en modelos.


# En resumen, utilizarás Form cuando necesites formularios personalizados no relacionados con un modelo específico, forms.ModelForm 
# cuando desees aprovechar la integración con modelos de base de datos existentes y CBV cuando quieras estructurar tus vistas utilizando clases, 
# aprovechando la funcionalidad incorporada en las clases de vista de Django. La elección dependerá de los requisitos específicos de tu proyecto y 
# del nivel de personalización y funcionalidad que necesites implementar.

class HorarioSemestralForm(forms.ModelForm): #ModelForm

    #para el id_funcionario_docente generamos un campo modelchoicefield e indicamos que este desabilitado y no sea requerido en el template, el queryset dejamos vacio aqui.. y el valor predeterminado el primer valor
    #y lo sobreescribimos en el constructor para asignar el valor id_funcionario_docente del usuario logeado. 

    #sacamos de manera momentanea el valor inicia para poder hacer las migraciones correctamente, luego volvemos a poner cuando ya hayamos migrado
    id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', widget=forms.Select(attrs={'class': 'form-control'}), initial=FuncionarioDocente.objects.first())
    #id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', initial=FuncionarioDocente.objects.first(), widget=forms.Select(attrs={'class': 'form-control'}))
    #id_funcionario_docente= forms.CharField(label='id_funcionario_docente', widget=forms.TextInput(attrs={"class": "hidden"}), disabled= True, required= False)
    id_convocatoria = forms.ModelChoiceField(label='id_convocatoria', queryset= Convocatoria.objects.all().order_by('-anho'), to_field_name= 'id_convocatoria', widget=forms.Select(attrs={'class': 'form-control'}))
    id_dia = forms.ModelChoiceField(label='id_dia', queryset= Dia.objects.all(), to_field_name= 'id_dia', widget=forms.Select(attrs={'class': 'form-control'}))
    hora_inicio= forms.TimeField(label= 'hora_inicio', widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}, format="%H:%M"))
    hora_fin= forms.TimeField(label= 'hora_fin', widget= forms.TimeInput(attrs={"type": "time", "class": "form-control"}, format="%H:%M"))

    class Meta:
        model = HorarioSemestral
        fields = ["id_funcionario_docente", "id_convocatoria", "id_dia","hora_inicio", "hora_fin"]

    #validamos que ya no exista registro para el mismo func/doc en el rango de horas para el mismo dia y convocatoria.
    def clean(self):
        cleaned_data = super().clean()
        id_funcionario_docente = cleaned_data.get('id_funcionario_docente')
        id_convocatoria = cleaned_data.get('id_convocatoria')
        id_dia = cleaned_data.get('id_dia')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if HorarioSemestral.objects.filter(id_funcionario_docente=id_funcionario_docente, id_convocatoria=id_convocatoria, id_dia=id_dia, hora_inicio= hora_inicio, hora_fin= hora_fin).exists():
            msg = 'Ya existe el rango de horas cargadas para el mismo dia y convocatoria.'
            self.add_error(None, msg)

        return cleaned_data
  
    # def __init__(self, *args, **kwargs):
    #     super(HorarioSemestralForm, self).__init__(*args, **kwargs)
    #     # input_formats to parse HTML5 datetime-local input to datetime field
    #     self.fields["hora_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
    #     self.fields["hora_fin"].input_formats = ("%Y-%m-%dT%H:%M",)
    
    # def clean_id_funcionario_docente(self, user, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     id_func_doc= FuncionarioDocente.objects.filter(id_funcionario_docente=user.id_persona)
    #     if id_funcionario_docente is not None:
    #         #dict = model_to_dict(per.first())
    #         # print("llego hasta validar el id persona")
    #         id_funcionario_docente = id_func_doc
    #         print("paso asignacion funcdoc")

    #     else:
    #         raise ValidationError("No es valido!")
    #     return id_funcionario_docente

    #este da error!
    # def clean_hora_inicio(self):
    #     hora_inicio = self.cleaned_data.get("hora_inicio")
    #     print(hora_inicio)
    #     hora_fin= self.cleaned_data.get("hora_fin")
    #     print(hora_fin)
    #     if hora_inicio > hora_fin:
    #         raise ValidationError("La hora de inicio no puede ser mayor que la fecha de fin.")
    #     return hora_inicio
    
    def clean_hora_fin(self):
        hora_inicio = self.cleaned_data.get("hora_inicio")
        hora_fin= self.cleaned_data.get("hora_fin")
        if hora_fin < hora_inicio:
            raise ValidationError("La hora de fin no puede ser menor que la fecha de inicio.")
        return hora_fin
    

    #sobreescribimos el valor del queryset 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(HorarioSemestralForm, self).__init__(*args, **kwargs)
        self.fields['id_funcionario_docente'].queryset = FuncionarioDocente.objects.filter(id_funcionario_docente=user.id_persona)
        # self.fields['id_funcionario_docente'].widget = forms.HiddenInput()
        #self.fields['id_funcionario_docente']= FuncionarioDocente.objects.filter(id_funcionario_docente=user.id_persona)

        #Guardamos el id_funcionario_docente del usuario actual
    # def save(self, *args, **kwargs):
    #     if not self.fields["id_funcionario_docente"]:  # si el objeto no ha sido guardado anteriormente
    #         print('entro al save')
    #         user = kwargs.pop('user')
    #         print(FuncionarioDocente.objects.filter(id_funcionario_docente=user.id_persona) )
    #         self.fields['id_funcionario_docente'].queryset = FuncionarioDocente.objects.filter(id_funcionario_docente=user.id_persona)  # obtiene el usuario actual
    #         super(HorarioSemestralForm, self).save(*args, **kwargs)  # llama al método save del modelo padrex





# class ActividadAcademica(forms.Form):
    
    #Event
    # id_estado_actividad_academica= forms.ModelChoiceField(label="Estado", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= EstadoActividadAcademica.objects.none(), required=False, to_field_name= 'id_estado_actividad_academica')
    # id_convocatoria= forms.ModelChoiceField(label="Convocatoria", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Convocatoria.objects.none(), required=False, to_field_name= 'id_convocatoria')
    # id_facultad= forms.ModelChoiceField(label='Facultad', queryset= Facultad.objects.all() , to_field_name= 'id_facultad', widget=forms.Select(attrs={'class': 'form-control'}))
    # id_materia= forms.ModelChoiceField(label='Materia', queryset= Materia.objects.none() , to_field_name= 'id_materia', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    # departamento= forms.ModelChoiceField(label='Departamento', queryset= Departamento.objects.none() , to_field_name= 'id_departamento', widget=forms.Select(attrs={'class': 'hidden'}), required=False)
    # id_funcionario_docente_encargado= forms.ModelChoiceField(label="Encargado", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= FuncionarioDocente.objects.none(), required=False, to_field_name= 'id_funcionario_docente')
    # id_persona_receptor = forms.ModelChoiceField(label='Receptor', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    # id_persona_alta= forms.ModelChoiceField(label="Solicitante", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Persona.objects.none(), required=False, to_field_name= 'id_persona')
    # datetime_inicio_estimado = forms.DateTimeField(label='Inicio Estimado', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_fin_estimado = forms.DateTimeField(label='Fin Estimado', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_inicio_real = forms.DateTimeField(label='Inicio Real', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_fin_real = forms.DateTimeField(label='Fin Real', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # observacion= forms.CharField(label='Observacion',widget= forms.Textarea(attrs={ "class": "form-control", "placeholder": "Desea agregar algun comentario adicional?"}))
    # nro_curso= forms.CharField(label='Nro. Curso',widget= forms.Textarea(attrs={ "class": "form-control", "placeholder": "Opcional"}))
    
    
    #DetalleActividadAcademica
    # id_detalle_actividad_Academica= forms.ModelChoiceField(label="Detalle", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= DetalleActividadAcademica.objects.none(), required=False, to_field_name= 'id_detalle_actividad_Academica')
    # id_participante= forms.ModelChoiceField(label="Participante", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Persona.objects.none(), required=False, to_field_name= 'id_persona')
    # id_actividad_academica= forms.ModelChoiceField(label="Actividad Academica", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Event.objects.none(), required=False, to_field_name= 'id_actividad_Academica')
    
    #Cita
    # id_cita= forms.ModelChoiceField(label="Cita", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Cita.objects.none(), required=False, to_field_name= 'id_cita')
    # id_parametro= forms.ModelChoiceField(label="Parametro", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Parametro.objects.none(), required=False, to_field_name= 'id_parametro')
    # es_tutoria= forms.BooleanField(label="Tutoria", widget=forms.TextInput(attrs={"class": "hidden"}), required=False)
    # es_orientacion_academica= forms.BooleanField(label="Orientacion Academica", widget=forms.TextInput(attrs={"class": "hidden"}), required=False)     
    # motivo = forms.CharField(label='Motivo', widget= forms.Textarea(attrs={ "class": "form-control", "placeholder": "Indique el motivo de la cita"}))
   
   
   
   
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['id_facultad'].widget.attrs['onchange'] = 'actualizar_campo_materia()'
        
    
    # def clean(self):
        
    #     dt_AA_facultad = self.cleaned_data['id_facultad']
    #     dt_AA_materia = self.cleaned_data['id_materia']
    #     dt_AA_receptor = self.cleaned_data['id_funcionario_docente']
        
    #      # Crear instancias de los modelos y guardar los datos
    #     modelo1 = Event(id_facultad= dt_AA_facultad, id_materia=dt_AA_materia, id_persona_receptor= dt_AA_receptor)
    #     modelo1.save()

        # modelo2 = Modelo2(id_materia=id_materia)
        # modelo2.save()

        # modelo3 = Modelo3(campo_modelo3=datos_modelo3)
        # modelo3.save()
        
        
        
#desde aqui voy a hacer una prueba para poder utilizar CVB's 

'''++++++++++++++++-------------------------------------------------------Calendario del Funcionario docente---------------------------------------------++++++++++++++++++++++'''
#Cita

class ActividadAcademicaForm(ModelForm):
    
    #indicamos los campos de pueden ser opcionales, aplica para todo el CRUD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observacion'].required = False
        self.fields['nro_curso'].required = False
        self.fields['id_materia'].required = False
        self.fields['id_departamento'].required = False
        self.fields['datetime_inicio_real'].required = False
        self.fields['datetime_fin_real'].required = False
        self.fields['id_facultad'].queryset = Facultad.objects.none()
        self.fields['id_facultad'].to_field_name = 'id_facultad'
        self.fields['id_materia'].queryset = Materia.objects.none()
        self.fields['id_materia'].to_field_name = 'id_materia'
        self.fields['id_funcionario_docente_encargado'].queryset = FuncionarioDocente.objects.none()
        self.fields['id_funcionario_docente_encargado'].to_field_name = 'id_funcionario_docente'
        
    # id_estado_actividad_academica= forms.ModelChoiceField(label="Estado", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= EstadoActividadAcademica.objects.none(), required=False, to_field_name= 'id_estado_actividad_academica')
    # id_convocatoria= forms.ModelChoiceField(label="Convocatoria", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Convocatoria.objects.none(), required=False, to_field_name= 'id_convocatoria')
    # id_facultad= forms.ModelChoiceField(label='Facultad', queryset= Facultad.objects.all() , to_field_name= 'id_facultad', widget=forms.Select(attrs={'class': 'form-control'}))
    # id_materia= forms.ModelChoiceField(label='Materia', queryset= Materia.objects.none() , to_field_name= 'id_materia', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    # departamento= forms.ModelChoiceField(label='Departamento', queryset= Departamento.objects.none() , to_field_name= 'id_departamento', widget=forms.Select(attrs={'class': 'hidden'}), required=False)
    # id_funcionario_docente_encargado= forms.ModelChoiceField(label="Encargado", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= FuncionarioDocente.objects.none(), required=False, to_field_name= 'id_funcionario_docente')
   # id_persona_alta= forms.ModelChoiceField(label="Solicitante", widget=forms.TextInput(attrs={"class": "hidden"}), queryset= Persona.objects.none(), required=False, to_field_name= 'id_persona')
    # datetime_inicio_estimado = forms.DateTimeField(label='Inicio Estimado', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_fin_estimado = forms.DateTimeField(label='Fin Estimado', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_inicio_real = forms.DateTimeField(label='Inicio Real', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # datetime_fin_real = forms.DateTimeField(label='Fin Real', widget= DateInput(attrs={"type": "datetime-local", "class": "hidden"}, format="%Y-%m-%dT%H:%M"), required=False)
    # observacion= forms.CharField(label='Observacion',widget= forms.Textarea(attrs={ "class": "form-control", "placeholder": "Desea agregar algun comentario adicional?"}))
    # nro_curso= forms.CharField(label='Nro. Curso',widget= forms.Textarea(attrs={ "class": "form-control", "placeholder": "Opcional"}))
    

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'id_facultad':  forms.Select(attrs={
            'autofocus': True,
            'class': 'form-control select2',
            'style': 'width: 100%'
            }),
            'id_materia':  forms.Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
            }),
            
            'id_funcionario_docente_encargado': forms.Select( attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
            }),
            'observacion': forms.Textarea(
                attrs={
                    'placeholder': 'Desea agregar algún comentario adicional?',
                    "class": "form-control",
                    'rows': 3,
                    'cols': 3,
                    "maxlength": 500
                }
            ),
            'nro_curso': forms.TextInput(attrs={
                'placeholder': 'Ingrese nro. de curso, opcional...',
                'class': 'form-control',
                "maxlength": 30
                
            })
        }
        
        
# class busquedaForm(Form):
    
#     facultades = forms.ModelChoiceField(queryset=Facultad.objects.none(), widget= forms.Select(attrs={
#         'class': 'form-control select2',
#         'style': 'width: 100%'
#     }))
    
#     materias = forms.ModelChoiceField(queryset=Materia.objects.all(), widget= forms.Select(attrs={
#         'class': 'form-control select2',
#         'style': 'width: 100%'
#     }))

#     funcionario_docente = forms.ModelChoiceField(queryset=FuncionarioDocente.objects.none(), widget= forms.Select(attrs={
#         'class': 'form-control select2',
#         'style': 'width: 100%'
#     }))


class ReportForm(Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    id_facultad = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    id_materia = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    id_funcionario_docente_encargado = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    id_estado = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    id_persona_solicitante = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    id_tipo_tutoria = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    
