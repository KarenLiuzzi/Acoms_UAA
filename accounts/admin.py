from django.contrib import admin
from accounts.models.user import Persona, TipoDocumento, Alumno, Funcionario, Docente, FuncionarioDocente, User

#registramos nuestros modelos en la pantalla de admin
admin.site.register(Persona)
admin.site.register(TipoDocumento)
admin.site.register(Alumno)
admin.site.register(Funcionario)
admin.site.register(Docente)
admin.site.register(FuncionarioDocente)
admin.site.register(User)