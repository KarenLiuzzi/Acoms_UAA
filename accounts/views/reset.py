from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
# from django.core.mail import send_mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# instalar en venv sendgrid> pip install -Iv sendgrid
from django.contrib.auth.decorators import login_required
from accounts.models.user import User
from accounts.forms import ResetPassForm, ResetPassConfirmation, ForgotPasswordTokenGenerator,CambiarContrasenha
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

#formulario de carga del correo para enviarle el token de restableciento
class ResetPassView(View):
    """ User reset password view """

    template_name = "accounts/password_reset_form.html"
    form_class = ResetPassForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            
            #enviamos el correo al usuario
            #obtenemos el mail y buscamos el objeto usuario
            destinatario= forms.cleaned_data['email']
            user =  User.objects.get(email= destinatario)
            #preparamos el token para el usuario
            reset_token_generator_object= ForgotPasswordTokenGenerator()
            password_reset_token= reset_token_generator_object.make_token(user)
            #verificar para no hacer de manera 
            base_url= 'http://127.0.0.1:8000/accounts/resetconfirm/'
            #base_url= reverse('resetconfirm', args=(user.pk, password_reset_token))
            forgot_password_urls= f'{base_url}{user.pk}/{password_reset_token}'
            #enviamos el correo
            enviarcorreo(forgot_password_urls, destinatario)
            return render(request, "accounts/password_reset_done.html") 

        #si so es valido volvemos a retonar el mismo objeto form para poder mostrar el error en pantalla    
        context = {"form": forms}
        return render(request, self.template_name, context)


#formulario de carga de correo para restablecer la contrasenha
class ResetPassConfirmView(View):
    """ User reset password view """

    template_name = "accounts/password_reset_confirm.html"
    form_class = ResetPassConfirmation

    pk= None
    reset_token_generator_object= None
    user= None

    #para mostrar el usuario, cuando se hace la llamada al base url
    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        try:
            #obtendremos los valores que recibira
            pk = kwargs.get('pk', None)
            password_reset_token = kwargs.get('password_reset_token', None)
            #si los datos son correctos se procede a validar si el token aun es valido para poder mostrar el formulario, caso contrario se direcciona al template de error
            if pk is not None or password_reset_token is not None:
                print("Value of 'pk' argument:", pk)
                print("Value of 'password_reset_token' argument:", password_reset_token)
                user= User.objects.get(pk= pk)
                reset_token_generator_object= ForgotPasswordTokenGenerator()
                if not reset_token_generator_object.check_token(user, password_reset_token):
                    print('Token Invalido')
                    #redireccionamos a la pantalla de error
                    return render(request, "accounts/error_token.html")
            else:
                print("No 'pk' argument was provided.")
                print("No 'password_reset_token' argument was provided.")                
                
        except Exception as e:
            print(e)
            #redireccionamos a la pantalla de error
            return render(request, "accounts/error_token.html")
        return render(request, self.template_name, context)

    #*args es para pasar n cantidad de parametros pero sin nombre(es na tupla), *kwargs se utiliza para recibir n cantidad de parametros pero con nombre, seria un diccionario
    #esto es para poder guardar lo que esta cargado en el formulario    
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid(): 
            #obtendremos los valores que recibira
            pk = kwargs.get('pk', None)
            password_reset_token = kwargs.get('password_reset_token', None)
            #si los datos son correctos procedemos a guardar el objeto actualizado
            if pk is not None or password_reset_token is not None:
                print("Value of 'pk' argument:", pk)
                print("Value of 'password_reset_token' argument:", password_reset_token)
                user= User.objects.get(pk= pk)
                user.set_password(forms.cleaned_data["password1"])
                user.save()
                #redireccionamos al inicio de sesion
                return redirect("accounts:signin")
        #si so es valido volvemos a retonar el mismo objeto form para poder mostrar el error en pantalla    
        context = {"form": forms}
        return render(request, self.template_name, context)


#configurar el setting.py, crear logica de envio de correo, obtener el mail del token
def enviarcorreo(forgot_password_urls, destinatario):
    message= Mail(
        from_email= 'beatrizmoon@hotmail.com' ,
        to_emails= destinatario,
        subject= 'Restauración de Contraseña, Sistema AcOms',
        html_content= f'A continuación un enlace que le ayudara restablecer su contraseña: <br> <a href= "{forgot_password_urls}"> Click aqui para Restaurar su contraseña </a> <br> Atte equipo AcOms.'
    )

    try:
        #si es necesario hacer la obtencion del token con una variable global 
        sg= SendGridAPIClient(os.environ.get('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'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

#@login_required
#este me esta causando errores!
class CambiarContrasenhaView(LoginRequiredMixin, View):

    template_name = "accounts/cambiar_contrasenha.html"
    form_class = CambiarContrasenha

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    #aqui procedemos a hacer el cambio
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid(): 

            #aqui debemos validar si la contrasenha ingresada es el mismo que el usuario logeado actualmente
            current_user = request.user
            senha= forms.cleaned_data["contrasenha"]
            if current_user.check_password(senha):
                # Contraseña correcta
                current_user.set_password(forms.cleaned_data["password1"])
                current_user.save()
                #actualizamos los datos de la sesion actual 
                update_session_auth_hash(request, request.user)
                #ver que hacer una vez que ya este finalizado!
                return HttpResponse(status= 204) #No content
            else:
                messages.error(request, 'Los datos son incorrectos, vuelve a intentarlo.')
                messages.clear()

        #si so es valido volvemos a retonar el mismo objeto form para poder mostrar el error en pantalla
        context = {"form": forms}
        return render(request, self.template_name, context)
    