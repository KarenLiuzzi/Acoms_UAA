from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from accounts.models.user import Persona


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class SignUpForm(forms.ModelForm):
    #Los atributos (attrs) en Django se utilizan para establecer valores predeterminados para los campos de un formulario o widget. 
    #Los atributos también se pueden utilizar para establecer el estilo CSS o la clase CSS de un campo o widget.

    documento = forms.CharField(
        label="documento",
        widget=forms.TextInput(attrs={"class": "form-control"}), error_messages= {'required': 'Por favor ingrese su Nro de Documento'}, strip= True
    )
    
    id_persona = forms.CharField(
        label="id_persona",
        widget=forms.TextInput(attrs={"class": "hidden"}),
        disabled= True, required= False,
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    """La clase Meta en Django se utiliza para establecer opciones adicionales en un modelo, como el orden de clasificación 
    predeterminado, si el modelo se debe utilizar en la administración de Django o si se deben crear tablas en la base de datos 
    para el modelo. Por ejemplo, si desea establecer el orden predeterminado de clasificación para un modelo en orden descendente 
    por fecha de creación, podría definir una clase Meta en su modelo con la opción 'ordering' establecida en '-created_at'."""
    class Meta:
        model = User
        fields = ["email", "documento", "id_persona"]
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"})}
    
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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las Contraseñas no coinciden!")
        return password2

    def save(self, commit=True):
        #En resumen, super() se utiliza para llamar a métodos o acceder a atributos de una clase base (padre) en una clase derivada(hijo).
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean_id_persona(self):
        doc = self.cleaned_data.get("documento")
        id = Persona.objects.filter(documento=doc)
        if id.exists():
            print("llego hasta validar el id persona")
            id_persona = id
            print("paso asignacion persona")
        else:
            raise ValidationError("No existe una persona con el Nro de documento en la Base de Datos!")
        return id_persona

#agregar para recuperar contrasenha
#para visualizar el perfil y cambiar la contrasenha