from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.core import validators

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
    id_facultad= models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carrera_facultad')
    descripcion_carrera= models.CharField(max_length=100)


    def __str__(self):
         return '%s - %s' % (self.id_facultad.descripcion_facultad, self.descripcion_carrera)

    class Meta:
        verbose_name_plural = "Carreras"

class Departamento(models.Model):
    id_departamento= models.AutoField(primary_key=True)
    id_facultad= models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='departamento_facultad')
    descripcion_departamento= models.CharField(max_length=100)
    telefono= models.CharField(max_length=10)

    def __str__(self):
         return '%s - %s' % (self.id_facultad.descripcion_facultad, self.descripcion_departamento)

    class Meta:
        verbose_name_plural = "Departamentos"

class Materia(models.Model):
    id_materia= models.AutoField(primary_key=True)
    id_departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='materia_departameto')
    descripcion_materia= models.CharField(max_length=100)

    def __str__(self):
         return '%s - %s' % (self.id_departamento.descripcion_departamento, self.descripcion_materia) or ''

    class Meta:
        verbose_name_plural = "Materias"

class Persona(models.Model):
    id_tipo_documento= models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='tipo_documento')
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
        #eliminamos este elemento porque causa errores
        del item['carrera_alumno']
        item['id'] = self.id
        item['nombre'] = self.nombre
        item['apellido'] = self.apellido
        item['documento'] = self.documento
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
        
class MateriaCarrera(models.Model):
    id_materia_carrera=  models.AutoField(primary_key=True)
    id_carrera= models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='carreras_materias')
    id_materia= models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materias_carrera')

    def __str__(self):
         return '%s - %s' % (self.id_carrera.descripcion_carrera, self.id_carrera.descripcion_carrera)

    class Meta:
        verbose_name_plural = "Materias Carrera"

class Alumno(models.Model):
    id_alumno= models.ForeignKey(Persona, on_delete=models.CASCADE, primary_key=True, related_name='alumno')
    def __str__(self):
         return '%s %s' % (self.id_alumno.nombre, self.id_alumno.apellido)

    class Meta:
        verbose_name_plural = "Alumnos"

class FuncionarioDocente(models.Model):
    id_funcionario_docente= models.ForeignKey(Persona, on_delete=models.CASCADE, primary_key=True, related_name='funcionario_docente')
    id_departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE, null= True, related_name='departamento_funcionario_docente')
    id_facultad= models.ForeignKey(Facultad, on_delete=models.CASCADE, null= True, related_name='facultad_funcionario_docente')
    
    def __str__(self):
         return '%s %s' % (self.id_funcionario_docente.nombre, self.id_funcionario_docente.apellido)


    class Meta:
        verbose_name_plural = "Funcionarios/Docentes"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(id_departamento__isnull=False, id_facultad__isnull=False),
                name='departamento_facultad_constraint',
            )
        ]

class Docente(models.Model):
    id_docente= models.ForeignKey(FuncionarioDocente, on_delete=models.CASCADE, primary_key=True, related_name='docente')
    def __str__(self):
         return '%s %s' % (self.id_docente.id_funcionario_docente.nombre, self.id_docente.id_funcionario_docente.apellido)

    class Meta:
        verbose_name_plural = "Docentes"

class Funcionario(models.Model):
    id_funcionario= models.ForeignKey(FuncionarioDocente, on_delete=models.CASCADE, primary_key=True, related_name='funcionario')
    def __str__(self):
         return '%s %s' % (self.id_funcionario.id_funcionario_docente.nombre, self.id_funcionario.id_funcionario_docente.apellido)

    class Meta:
        verbose_name_plural = "Funcionarios"



"""" BaseUserManager es una clase base que proporciona una implementación básica de un administrador de usuarios,
es utilizado cuando se usa AbstractBaseUser para crear una clase de usuario personalizada, para que se pueda proporcionar un
administrador de usuarios personalizado que sepa cómo tratar con esa clase de usuario específica. """

class UserManager(BaseUserManager):
    """ User manager solo va contener los metodos, no los atributos, un metodo para crear un usurio nomarl y otro par crer un super user """
    # kwarg, te permite pasar un número arbitrario de argumentos de palabras clave. Puedes pasar cualquier otro campo a la función y se guardará en tu modelo si existe con el mismo nombre.
    def _create_user(self, email, password=None,**extra_fields):
        """Creates and returns a new user using an email address"""
        if not email:  # check for an empty email
            raise AttributeError("El campo email es obligatorio")
        else:  # normalizes the provided email
            #normalize pone en minusculas
            email = self.normalize_email(email)

        # Verifica si el campo documento existe en Persona
        documento = extra_fields.get('documento')
        if not documento or documento== "":
            raise AttributeError("El campo documento es obligatorio")
        else:
            try:
                #verificamos que no exista un usuario con el mismo documento 
                usuario= User.objects.filter(documento= documento)
                if usuario.exists():
                    raise AttributeError("Ya existe un usuario con el documento ingresado")
                else:
                    persona = Persona.objects.get(documento=documento)
                    extra_fields['id_persona'] = persona
            except Persona.DoesNotExist:
                raise ValueError('El documento no existe en la tabla Persona')

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
    documento= models.CharField(max_length=30, unique= True, validators=[
            validators.RegexValidator(
                regex=r'^\d{1,10}$',
                message='El documento debe ser un número de hasta 10 dígitos.'
            ),
        ]) #blank=True, null= True)
    id_persona= models.ForeignKey(Persona, on_delete=models.CASCADE,  related_name='usuario', blank= True, null= True)
    materia_func_doc= models.ManyToManyField(Materia, blank=True, help_text='Las materias asignadas al Funcionario/Docente', related_name='func_doc_materias') #, through= 'MateriaFuncionarioDocente') no funciona con este en el panel de admin
    #carrera_usuario= models.ManyToManyField(Carrera, blank=True, help_text='Las carreras asignadas al usuario', related_name='user_carreras')
    lector =  models.BooleanField(default=True)
    
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
    REQUIRED_FIELDS = ['documento']

    def __str__(self):
         return '%s' % (self.email)


    class Meta:
        verbose_name_plural = "Usuarios"
