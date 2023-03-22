from django.forms import ModelForm, DateInput, TimeInput
from calendarapp.models import Event, EventMember
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from accounts.models.user import FuncionarioDocente
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]

# En resumen, la principal diferencia entre "forms.ModelForm" y "ModelForm" es que "forms.ModelForm" es una clase que 
# ofrece algunas funcionalidades adicionales para personalizar la representación y validación de los campos del formulario,
# mientras que "ModelForm" es una clase más simple que se utiliza para crear formularios basados en modelos.

# se puede hacer un search filter drop down con model form en django?
class HorarioSemestralForm(forms.ModelForm): #ModelForm
    class Meta:
        model = HorarioSemestral
        #fields = ["id_funcionario_docente", "id_convocatoria", "id_dia","hora_inicio", "hora_fin"]
        fields = '__all__'

    #funcionario_docente = forms.ModelChoiceField(label='Funcionario Docente', queryset= FuncionarioDocente.objects.filter(), to_field_name= 'id_convocatoria', to_field_name= 'id_funcionario_docente')
    convocatoria = forms.ModelChoiceField(label='Convocatoria', queryset= Convocatoria.objects.all(), to_field_name= 'id_convocatoria')
    dia = forms.ModelChoiceField(label='Dia', queryset= Dia.objects.all(), to_field_name= 'id_dia')
    hora_inicio= forms.TimeField(widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}, format="%H:%M"))
    hora_fin= forms.TimeField(widget= forms.TimeInput(attrs={"type": "time", "class": "form-control"}, format="%H:%M"))

    def __init__(self, *args, **kwargs):
        super(HorarioSemestralForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["hora_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["hora_fin"].input_formats = ("%Y-%m-%dT%H:%M",)
       
#para poder mostrar correctamente los datos tengo que crear una clase strin en cada modelo, en convo,dia