from django.forms import ModelForm, DateInput, ValidationError, Form
from calendarapp.models import Event, EventMember
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from accounts.models.user import FuncionarioDocente, Facultad, Materia
from django import forms


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

    #para el id_funcionario_docente generamos un campo modelchoicefield e indicamos que este desabilitado y no sea requerido en el template, el queryset dejamos vacio aqui..
    #y lo sobreescribimos en el constructor para asignar el valor id_funcionario_docente del usuario logeado. 

    #sacamos de manera momentanea el valor inicia para poder hacer las migraciones correctamente, luego volvemos a poner cuando ya hayamos migrado
    id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', widget=forms.Select(attrs={'class': 'form-control'}))
    #id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', initial=FuncionarioDocente.objects.first(), widget=forms.Select(attrs={'class': 'form-control'}))
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
    

'''++++++++++++++++-------------------------------------------------------Calendario del Funcionario docente---------------------------------------------++++++++++++++++++++++'''

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
    id_tipo_orientacion_academica = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    id_tipo_motivo = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    id_persona_responsable = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    id_persona_alta= forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
         'style': 'width: 100%'
    }))
    id_tipo_tarea = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    id_estado_tarea = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    
    
