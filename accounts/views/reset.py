from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from accounts.models.user import User
from accounts.forms import ResetPassForm, ResetPassConfirmation, ForgotPasswordTokenGenerator,CambiarContrasenha
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

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
            
            try:
                #enviamos el correo al usuario
                #obtenemos el mail y buscamos el objeto usuario
                destinatario= forms.cleaned_data['email']
                user =  User.objects.get(email= destinatario)
                #preparamos el token para el usuario
                reset_token_generator_object= ForgotPasswordTokenGenerator()
                password_reset_token= reset_token_generator_object.make_token(user)
                #verificar para no hacer de manera 
                base_url= 'http://127.0.0.1:8000/accounts/resetconfirm/'
                #base_url= reverse('resetconfirm')
                base_url= str(base_url)
                #base_url= reverse('resetconfirm', args=(user.pk, password_reset_token))
                forgot_password_urls= f'{base_url}{user.pk}/{password_reset_token}'
                #enviamos el correo
                enviarcorreo(forgot_password_urls, destinatario)
                return render(request, "accounts/password_reset_done.html") 
            except Exception as e:
                print(f"Se ha producido un error: {e}")

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
                user= User.objects.get(pk= pk)
                reset_token_generator_object= ForgotPasswordTokenGenerator()
                if not reset_token_generator_object.check_token(user, password_reset_token):
                    #redireccionamos a la pantalla de error
                    return render(request, "accounts/error_token.html")
            else:
                pass           
                
        except Exception as e:
            print(f"Se ha producido un error: {e}")
            return render(request, "accounts/error_token.html")
        return render(request, self.template_name, context)

    #*args es para pasar n cantidad de parametros pero sin nombre(es na tupla), *kwargs se utiliza para recibir n cantidad de parametros pero con nombre, seria un diccionario
    #esto es para poder guardar lo que esta cargado en el formulario    
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid(): 
            try:
                #obtendremos los valores que recibira
                pk = kwargs.get('pk', None)
                password_reset_token = kwargs.get('password_reset_token', None)
                #si los datos son correctos procedemos a guardar el objeto actualizado
                if pk is not None or password_reset_token is not None:
                    #print("Value of 'pk' argument:", pk)
                    #print("Value of 'password_reset_token' argument:", password_reset_token)
                    user= User.objects.get(pk= pk)
                    user.set_password(forms.cleaned_data["password1"])
                    user.save()
                    #redireccionamos al inicio de sesion
                    return redirect("accounts:signin")
            except Exception as e:
                print(f"Se ha producido un error: {e}")
        #si so es valido volvemos a retonar el mismo objeto form para poder mostrar el error en pantalla    
        context = {"form": forms}
        return render(request, self.template_name, context)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#configurar el setting.py, crear logica de envio de correo, obtener el mail del token
def enviarcorreo(forgot_password_urls, destinatario):
    # Configura tus credenciales de Outlook
    sender_email = 'kaliuzzi@uaa.edu.py'
    sender_password = 'Yad92906'

    # Configura el servidor SMTP de Outlook
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587  # Puerto de Outlook para TLS (587)

    # Crea un objeto SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Inicia la conexión TLS (segura)
    server.starttls()

    # Inicia sesión en tu cuenta de Outlook
    server.login(sender_email, sender_password)

    # Crea el mensaje de correo con contenido HTML
    subject = 'Restablecer contraseña'
    recipient_email = destinatario

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Cuerpo del correo en formato HTML con la variable
    html_body = f"""
    <html>
    <body>
        <p>A continuación, un enlace que te ayudará a restablecer tu contraseña:</p>
        <p><a href="{forgot_password_urls}">Haz clic <strong>aquí</strong> para restablecer tu contraseña</a></p>
        <p>Atentamente,</p>
        <p>Equipo AcOms</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Envía el correo
        server.sendmail(sender_email, recipient_email, msg.as_string())
        # Cierra la conexión SMTP
        server.quit()
        print('Correo enviado con éxito')
    except Exception as e:
        print(f"Se ha producido un error: {e}")
            
#anterior        
# def enviarcorreo(forgot_password_urls, destinatario):
#     message= Mail(
#         from_email= 'beatrizmoon@hotmail.com' ,
#         to_emails= destinatario,
#         subject= 'Restauración de Contraseña, Sistema AcOms',
#         html_content= f'A continuación un enlace que le ayudara restablecer su contraseña: <br> <a href= "{forgot_password_urls}"> Click aqui para Restaurar su contraseña </a> <br> Atte equipo AcOms.'
#     )

#     try:
#         #si es necesario hacer la obtencion del token con una variable global 
#         sg= SendGridAPIClient(os.environ.get('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'))
#         response = sg.send(message)
#     except Exception as e:
#         print(f"Se ha producido un error: {e}")


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
            try:
                storage = messages.get_messages(request)
                for message in storage:
                    if message.level == messages.ERROR:
                        storage.discard(message)

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
            except Exception as e:
                print(f"Se ha producido un error: {e}")

        #si so es valido volvemos a retonar el mismo objeto form para poder mostrar el error en pantalla
        context = {"form": forms}
        return render(request, self.template_name, context)
    