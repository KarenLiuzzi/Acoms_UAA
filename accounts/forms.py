from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.models import User
from accounts.models.user import Persona

#from django.forms.models import model_to_dict

def clean_email(mail):
        user = User.objects.filter(email= mail)
        #Validamos si existe un usuario con el mail
        if user.count() == 0:

            raise ValidationError("No existe un usuario registrado con el correo electrónico!")
            
        else:
            return mail

def validar_mail(mail):
        user = User.objects.filter(email= mail)
        #Validamos si existe un usuario con el mail
        if user.count() == 0:
            raise ValidationError("Los datos son incorrectos, vuelve a intentarlo.")
        return mail



class ResetPassConfirmation(forms.Form):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password])

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        #if password1 and password2 and password1 != password2:
        if password1 != password2:
            raise ValidationError("Las Contraseñas no coinciden!")
        return password2    

class ResetPassForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), validators=[clean_email])

class SignInForm(forms.Form):

    # def clean(self):
    #     cleaned_data = super().clean()

    # def clean_password(self):
    #     user = User.objects.get(mail= self.cleaned_data.get("email"))

    #     if user.check_password():
    #         # Contraseña correcta
    #         return self.cleaned_data.get("password")
    #     else:
    #         raise ValidationError("Los datos son incorrectos, vuelve a intentarlo.")
        

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), validators=[validar_mail])
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
        label="id_persona", required= False,
        widget=forms.TextInput(attrs={"class": "hidden"}),
    )
    
    # materia_func_doc = forms.ModelMultipleChoiceField(queryset= Persona.objects.none(),
    #     widget=forms.SelectMultiple(attrs={"class": "hidden"}), required= False
    # )
    
    #email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={"class": "form-control"}), validators=[validar_mail])
    
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
        #if user_doc.exists():
        if user_doc.count() != 0:
            raise ValidationError("Ya existe un usuario con el Nro de Cédula!")
        return doc

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        #if password1 and password2 and password1 != password2:
        if password1 != password2:
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
        per = Persona.objects.filter(documento=doc).first()
        #print(per)
        # if per is not None:
        if per is not None:
            #dict = model_to_dict(per.first())
            # print("llego hasta validar el id persona")
            id_persona = per
            #print("paso asignacion persona")

        else:
            raise ValidationError("No existe una persona con el Nro de documento en la Base de Datos!")
        return id_persona
    
    # def clean_materia_func_doc(self):
    #     materia_func_doc = self.cleaned_data.get("materia_func_doc")
    #     #per = Persona.objects.filter(documento=doc).first()
    #     #print(per)
    #     # if per is not None:
    #     if materia_func_doc is  None:
    #     #     #dict = model_to_dict(per.first())
    #     #     # print("llego hasta validar el id persona")
    #     #     print(materia_func_doc)
    #     #     #print("paso asignacion persona")

    #     # else:
    #         print(materia_func_doc)
    #         raise ValidationError("Existe un problema con materia_func_doc!")
            
    #     return materia_func_doc

#clase para generar el token de reset pass a el usuario
class ForgotPasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp= (
            ''
            if user.last_login is None 
            else user.last_login.replace(microsecond= 0, tzinfo= None)
        )
        return f'{user.pk} {user.password} {login_timestamp} {timestamp}'


class CambiarContrasenha(forms.Form):
    contrasenha = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password])

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        contrasenha= self.cleaned_data.get("contrasenha")
        #if password1 and password2 and password1 != password2:
        if password1 != password2:
            raise ValidationError("Las Contraseñas no coinciden!")
        elif (contrasenha == password1 or contrasenha == password2):
            raise ValidationError("La Contraseña debe ser diferente!")
        return password2    
