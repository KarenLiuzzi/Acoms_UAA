from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

class TipoDocumento(models.Model):
    descripcion_tipo_documento = models.CharField(max_length=30, unique= True)

    def __str__(self):
        return '%s' % (self.descripcion_tipo_documento)

    class Meta:
        verbose_name_plural = "Tipos de documento"
        
class Facultad(models.Model):
    id_facultad= models.AutoField(primary_key=True)
    descripcion_facultad= models.CharField(max_length=60)

    def __str__(self):
         return '%s' % (self.descripcion_facultad)

    class Meta:
        verbose_name_plural = "Facultades"
        
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
class Carrera(models.Model):
    id_carrera= models.AutoField(primary_key=True)
    id_facultad= models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name='carrera_facultad')
    descripcion_carrera= models.CharField(max_length=100)


    def __str__(self):
         return '%s - %s' % (self.id_facultad.descripcion_facultad, self.descripcion_carrera)

    class Meta:
        verbose_name_plural = "Carreras"

class Departamento(models.Model):
    id_departamento= models.AutoField(primary_key=True)
    id_facultad= models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name='departamento_facultad')
    descripcion_departamento= models.CharField(max_length=100)
    telefono= models.CharField(max_length=10)

    def __str__(self):
         return '%s - %s' % (self.id_facultad.descripcion_facultad, self.descripcion_departamento)

    class Meta:
        verbose_name_plural = "Departamentos"

class Materia(models.Model):
    id_materia= models.AutoField(primary_key=True)
    id_departamento= models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='materia_departameto')
    descripcion_materia= models.CharField(max_length=100)

    def __str__(self):
         return '%s - %s' % (self.id_departamento.descripcion_departamento, self.descripcion_materia) or ''

    class Meta:
        verbose_name_plural = "Materias"

class Persona(models.Model):
    id_tipo_documento= models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='tipo_documento')
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    documento= models.CharField(max_length=30, unique= True)
    correo= models.CharField(max_length=50, blank= True)
    telefono= models.CharField(max_length=30, blank= True)
    celular= models.CharField(max_length=30, blank= True)
    carrera_alumno= models.ManyToManyField(Carrera, blank=True, help_text='Las carreras asignadas al alumno', related_name='alumno_carrera', through= 'CarreraAlumno')

    def __str__(self):
        return '%s %s %s' % (self.nombre, self.apellido, self.documento)
    
    def toJSON(self):
        item = model_to_dict(self)
        # item['nombre'] = self.nombre
        # item['apellido'] = self.apellido
        # item['documento'] = self.documento
        return item

    class Meta:
        verbose_name_plural = "Personas"
        
class CarreraAlumno(models.Model):
    id_carrera_alumno=  models.AutoField(primary_key=True)
    id_carrera= models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='carrera_alumno')
    id_alumno= models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='alumno_carrera')

    def __str__(self):
         return '%s - %s' % (self.id_carrera.descripcion_carrera, self.id_alumno)

    class Meta:
        verbose_name_plural = "Carreras Alumno"

class Alumno(models.Model):
    id_alumno= models.ForeignKey(Persona, on_delete=models.PROTECT, primary_key=True, related_name='alumno')
    def __str__(self):
         return '%s %s' % (self.id_alumno.nombre, self.id_alumno.apellido)

    class Meta:
        verbose_name_plural = "Alumnos"

class FuncionarioDocente(models.Model):
    id_funcionario_docente= models.ForeignKey(Persona, on_delete=models.PROTECT, primary_key=True, related_name='funcionario_docente')
    def __str__(self):
         return '%s %s' % (self.id_funcionario_docente.nombre, self.id_funcionario_docente.apellido)

    class Meta:
        verbose_name_plural = "Funcionarios/Docentes"

class Docente(models.Model):
    id_docente= models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, primary_key=True, related_name='docente')
    def __str__(self):
         return '%s %s' % (self.id_docente.id_funcionario_docente.nombre, self.id_docente.id_funcionario_docente.apellido)

    class Meta:
        verbose_name_plural = "Docentes"

class Funcionario(models.Model):
    id_funcionario= models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, primary_key=True, related_name='funcionario')
    def __str__(self):
         return '%s %s' % (self.id_funcionario.id_funcionario_docente.nombre, self.id_funcionario.id_funcionario_docente.apellido)

    class Meta:
        verbose_name_plural = "Funcionarios"



"""" En resumen, BaseUserManager es una clase base que proporciona una implementación básica de un administrador de usuarios,
es utilizado cuando se usa AbstractBaseUser para crear una clase de usuario personalizada, para que se pueda proporcionar un
administrador de usuarios personalizado que sepa cómo tratar con esa clase de usuario específica. """

class UserManager(BaseUserManager):
    """ User manager solo va contener los metodos, no los atributos, un metodo para crear un usurio nomarl y otro par crer un super user """
    # kwarg, te permite pasar un número arbitrario de argumentos de palabras clave. Puedes pasar cualquier otro campo a la función y se guardará en tu modelo si existe con el mismo nombre.
    def _create_user(self, email, password=None,**extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise AttributeError("User must set an email address")
        else:  # normalizes the provided email
            #normalize pone en minusculas
            email = self.normalize_email(email)

        # create user
        user = self.model(email=email, **extra_fields)
        #va a encriptar el pass
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        return user

    #kwards También se utiliza para acceder a los campos incorporados del modelo de usuario por defecto como is_superuser,is_staff y is_active y asignarles un valor por defecto.
    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)

#heredando del abstactbaseuser a user nos permitira customizar/editar completamente todo el custom user model, incluyendo la funcionalidad de authentication
#tambien hay otro llamado abstractuser que se nos permite agregar mas campos pero en cambio no tendremos la ventaja de controlar como en el abstractbaseuser
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model, contendra los campos"""
    documento= models.CharField(max_length=30, unique= True, blank=True, null= True)
    id_persona= models.ForeignKey(Persona, on_delete=models.PROTECT,  related_name='usuario', blank= True, null= True)
    materia_func_doc= models.ManyToManyField(Materia, blank=True, help_text='Las materias asignadas al Funcionario/Docente', related_name='func_doc_materias') #, through= 'MateriaFuncionarioDocente') no funciona con este en el panel de admin
    #carrera_usuario= models.ManyToManyField(Carrera, blank=True, help_text='Las carreras asignadas al usuario', related_name='user_carreras')

    email = models.EmailField(
        _("Email Address"),
        max_length=255,
        unique=True,
        help_text="Ex: example@example.com",
    )

    is_staff = models.BooleanField(_("Staff status"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
#comentamos para ver como devuelve al instanciar el objeto con un campo en un queryset
    # def __str__(self):
    #     return self.email

    # def __str__(self):
    #     field_values = []
    #     for field in self._meta.get_fields():
    #         field_values.append(str(getattr(self, field.name, '')))
    #     return ' '.join(field_values)
    # def __str__(self):
    #      return '%s %s %s %s %s' % (self.email, self.id_persona, self.documento, self.is_staff, self.is_superuser)
    def __str__(self):
         return '%s' % (self.email)

    REQUIRED_FIELDS= ['documento']

    class Meta:
        verbose_name_plural = "Usuarios"


#probar como solicitar campo de documento en creacion de superuser


#hacemos las tablas de muchos a muchos y Mate. Usuario
#comentamos xq en el panel de admin no funcionas
# class MateriaFuncionarioDocente(models.Model):
#     id_materia_funcionario_docente=  models.AutoField(primary_key=True)
#     id_materia= models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materia_funcionario_docente')
#     id_funcionario_docente= models.ForeignKey(User, on_delete=models.CASCADE, related_name='funcionario_docente_materia')

#     def __str__(self):
#          return '%s - %s' % (self.id_materia.descripcion_materia, self.id_funcionario_docente.id_funcionario_docente.documento)

#     class Meta:
#         verbose_name_plural = "Materias Funcionario/Docente"