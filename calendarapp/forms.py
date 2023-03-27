from time import strptime
from django.forms import ModelForm, DateInput, TimeInput, ValidationError
from requests import request
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


class HorarioSemestralForm(forms.ModelForm): #ModelForm

    #para el id_funcionario_docente generamos un campo modelchoicefield e indicamos que este desabilitado y no sea requerido en el template, el queryset dejamos vacio aqui.. y el valor predeterminado el primer valor
    #y lo sobreescribimos en el constructor para asignar el valor id_funcionario_docente del usuario logeado. 

    id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', initial=FuncionarioDocente.objects.first(), widget=forms.Select(attrs={'class': 'form-control'}))
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


    