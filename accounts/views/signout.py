from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings

def signout(request):
    logout(request)
    #return redirect(settings.LOGOUT_REDIRECT_URL)
    return redirect("accounts:signin")
