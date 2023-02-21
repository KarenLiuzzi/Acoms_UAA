from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models.user import Persona
from django.forms.models import model_to_dict

from accounts.forms import SignUpForm

#login_required, garantiza que el usuario esté autenticado antes de que se ejecute la vista.
@login_required
def ProfileView(request):

    current_user = request.user
    #https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
    dict = model_to_dict(current_user)
    persona=  Persona.objects.get(pk= dict["id_persona"])
    context = {"user": current_user, "persona": persona}

    return render(request, "accounts/profile.html", context)
