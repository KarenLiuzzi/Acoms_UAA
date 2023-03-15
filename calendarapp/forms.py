from django.forms import ModelForm, DateInput, TimeInput
from calendarapp.models import Event, EventMember
from calendarapp.models.calendario import HorarioSemestral
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

# se puede hacer un search filter drop down con model form en django?
class CalendarioForm(ModelForm):
    class Meta:
        model = HorarioSemestral
        fields = ["id_funcionario_docente", "id_convocatoria", "id_dia","hora_inicio", "hora_fin"]

        id_funcionario_docente = forms.IntegerField(widget=forms.HiddenInput())
        id_convocatoria = forms.IntegerField(widget=forms.HiddenInput())
        #descripcion_convocatoria = forms.CharField(disabled=True)
        id_dia = forms.IntegerField(widget=forms.HiddenInput())
        #descripcion_dia = forms.CharField(disabled=True)

        # datetime-local is a HTML5 input type
        widgets = {
            # "title": forms.TextInput(
            #     attrs={"class": "form-control", "placeholder": "Enter event title"}
            # ),
            # "description": forms.Textarea(
            #     attrs={
            #         "class": "form-control",
            #         "placeholder": "Enter event description",
            #     }
            # ),
            "hora_inicio": TimeInput(
                attrs={"type": "time", "class": "form-control"},
                format="%H:%M",
            ),
            "hora_fin": TimeInput(
                attrs={"type": "time", "class": "form-control"},
                format="%H:%M",
            ),
        }
        #exclude = ["user"]