from django.views.generic import View
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm
from django.conf import settings


class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            # print("antes de asignar valor al ID")
            # forms.id_persona= 1
            # print("formulario validado")
            forms.save()
            return redirect("accounts:signin")
            #return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            for field, errors in forms.errors.items():
                for error in errors:
                    print(f"Error en el campo {field}: {error}")
                    
        context = {"form": forms}
        return render(request, self.template_name, context)
