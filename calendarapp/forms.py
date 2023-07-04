from time import strptime
from django.forms import ModelForm, DateInput, TimeInput, ValidationError
from requests import request
from calendarapp.models import Event, EventMember
from calendarapp.models.calendario import HorarioSemestral, Dia, Convocatoria
from accounts.models.user import FuncionarioDocente, Facultad, Materia
from django import forms

#el parametro cargaremos en minutos y ese vamos a tomar como valor para poder calcular el tiempo entre horarios del funcionario/docente
from datetime import datetime, timedelta

def dividir_fechas_en_minutos(fecha1, fecha2, minutos):
    # Convertir las fechas de strings a objetos datetime
    fecha1 = datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
    fecha2 = datetime.strptime(fecha2, '%Y-%m-%d %H:%M:%S')

    # Calcular la diferencia en minutos
    diferencia = fecha2 - fecha1
    minutos_totales = int(diferencia.total_seconds() / 60)

    # Dividir la diferencia en minutos según el tercer parámetro
    divisiones = []
    for i in range(minutos, minutos_totales + minutos, minutos):
        fecha_division = fecha1 + timedelta(minutes=i)
        divisiones.append(fecha_division)

    return divisiones

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


class HorarioSemestralForm(forms.ModelForm): #ModelForm

    #para el id_funcionario_docente generamos un campo modelchoicefield e indicamos que este desabilitado y no sea requerido en el template, el queryset dejamos vacio aqui.. y el valor predeterminado el primer valor
    #y lo sobreescribimos en el constructor para asignar el valor id_funcionario_docente del usuario logeado. 

    #sacamos de manera momentanea el valor inicia para poder hacer las migraciones correctamente, luego volvemos a poner cuando ya hayamos migrado
    id_funcionario_docente = forms.ModelChoiceField(label='id_funcionario_docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', widget=forms.Select(attrs={'class': 'form-control'}))
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


class SolicitarCita(forms.Form):
    
    id_facultad= forms.ModelChoiceField(label='Facultad', queryset= Facultad.objects.all() , to_field_name= 'id_facultad', widget=forms.Select(attrs={'class': 'form-control'}))
    #departamento= forms.ModelChoiceField(label='Departamento', queryset= Departamento.objects.none() , to_field_name= 'id_departamento', widget=forms.Select(attrs={'class': 'form-control'}))
    id_materia= forms.ModelChoiceField(label='Materia', queryset= Materia.objects.none() , to_field_name= 'id_materia', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    id_persona_receptor = forms.ModelChoiceField(label='Docente', queryset= FuncionarioDocente.objects.none() , to_field_name= 'id_funcionario_docente', widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['id_facultad'].widget.attrs['onchange'] = 'actualizar_campo_materia()'
        
    
    def clean(self):
        
        dt_AA_facultad = self.cleaned_data['id_facultad']
        dt_AA_materia = self.cleaned_data['id_materia']
        dt_AA_receptor = self.cleaned_data['id_funcionario_docente']
        
         # Crear instancias de los modelos y guardar los datos
        modelo1 = Event(id_facultad= dt_AA_facultad, id_materia=dt_AA_materia, id_persona_receptor= dt_AA_receptor)
        modelo1.save()

        # modelo2 = Modelo2(id_materia=id_materia)
        # modelo2.save()

        # modelo3 = Modelo3(campo_modelo3=datos_modelo3)
        # modelo3.save()
