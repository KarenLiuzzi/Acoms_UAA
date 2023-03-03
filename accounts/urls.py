from django.urls import path

from accounts import views
from accounts.views import reset, profile

app_name = "accounts"


urlpatterns = [
    path("reset/", reset.ResetPassView.as_view(), name='reset'),
    path("resetconfirm/<str:pk>/<str:password_reset_token>", reset.ResetPassConfirmView.as_view(), name='resetconfirm'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path("profile/", profile.ProfileView, name="profile"),
    path("cambiarcontrasenha/", reset.CambiarContrasenhaView.as_view(), name="cambiarcontrasenha"),
    
]
