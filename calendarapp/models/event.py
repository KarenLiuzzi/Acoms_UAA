from datetime import datetime
from django.db import models
from django.urls import reverse
from django.forms import model_to_dict
from calendarapp.models import EventAbstract
from accounts.models import User
from django.db.models import Q, CheckConstraint

"""models.Manager es una clase de Django que proporciona un mecanismo para realizar consultas a la base de datos y realizar operaciones en los modelos de manera más fácil y eficiente. Cada modelo de Django tiene al menos un objeto Manager asociado a él de forma predeterminada.

Los objetos Manager de los modelos de Django son responsables de proporcionar un conjunto de métodos para interactuar con la base de datos. Por ejemplo, objects.all() devuelve todos los registros de la base de datos para un modelo específico, mientras que objects.filter() permite realizar consultas más avanzadas para recuperar un subconjunto específico de registros.

También puedes crear tus propios objetos Manager personalizados para extender las funcionalidades por defecto y ajustar las consultas a tus necesidades específicas.

En resumen, models.Manager es un componente clave de Django que proporciona una API de consulta a la base de datos para modelos de Django, y permite interactuar de manera eficiente y efectiva con la información almacenada en la base de datos."""


class EventManager(models.Manager):
    """ Event manager. select_related: Sin embargo, debes tener en cuenta que esta optimización solo funciona para relaciones ForeignKey y OneToOneField. Si estás trabajando con relaciones ManyToManyField, deberás utilizar el método prefetch_related para optimizar las consultas. """
    #retornar todos los campos de un event
    # def get_cita(self, id):
    #     cita= Event.objects.filter(id_actividad_academica= id).values('id_estado_actividad_academica', 'id_actividad_academica').first
    #     return cita
    #este se usa para traer tanto las citas de tipo tutoria como de orientacion academica
    #def get_all_events(self, user):
    def get_all_events(self):
        
        #events = Event.objects.all() #.filter(user=user, is_active=True, is_deleted=False)
        events = Cita.objects.select_related("id_cita")

        return events
    """como hacer un inner join con dos modelos y obtener columnas seleccionadas con filtros especificos en django"""

    #este usamos para traer un solo tipo de cita, ya sea de tipo tutoria u orientacion academica -- ver como modificar
    #def get_running_events(self, user):
    def get_running_events(self, tipo_cita):
        if tipo_cita == 'Tutoria':
            
            running_events = Cita.objects.filter(es_tutoria= True).select_related("id_cita")
        elif tipo_cita== "OriAcademica":
            running_events = Cita.objects.filter(es_orientacion_academica= True).select_related("id_cita")
        else: 
            running_events = Cita.objects.select_related("id_cita")
            
        """ .filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")"""
        return running_events

"""Vamos a considerar que Event es la tabla de Actividad Academica"""
"""Modificaremos los nombres de los campos para que concidan con las de nuestro modelo"""
class EstadoActividadAcademica(models.Model):
    id_estado_actividad_academica= models.AutoField(primary_key=True)
    descripcion_estado_actividad_academica= models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion_estado_actividad_academica

from accounts.models.user import Facultad, Materia, Departamento, FuncionarioDocente, Persona
from calendarapp.models.calendario import Convocatoria



class Event(EventAbstract):
    """ Event model """

    id_estado_actividad_academica= models.ForeignKey(EstadoActividadAcademica, on_delete=models.PROTECT, related_name='estado_acti_aca')
    id_convocatoria= models.ForeignKey(Convocatoria, on_delete=models.PROTECT, related_name='convocatoria')
    id_facultad= models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name='facultad')
    id_materia= models.ForeignKey(Materia, on_delete=models.SET_NULL, blank=True, null=True)
    id_departamento= models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='departamento')
    id_funcionario_docente_encargado= models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, related_name='funcionario_docente_encarcado')
   #comento esto
    #id_persona_receptor= models.ForeignKey(Persona, on_delete=models.SET_NULL, related_name='persona_receptor', blank=True, null=True)
    id_persona_alta= models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='persona_alta')
    datetime_inicio_estimado = models.DateTimeField()
    datetime_fin_estimado = models.DateTimeField()
    datetime_inicio_real = models.DateTimeField(null= True, blank=True)
    datetime_fin_real = models.DateTimeField(null= True, blank=True)
    datetime_registro = models.DateTimeField() #auto_now=True
    observacion= models.CharField(max_length=500, null= True, blank=True)
    nro_curso= models.CharField(max_length=30, null= True, blank=True)
    #comento esto
    #participante_acti_academ= models.ManyToManyField(Persona, blank=True, help_text='Los participantes de la actividad academica', related_name='participante_acti_academica', through= 'DetalleActividadAcademica')

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    # title = models.CharField(max_length=200, unique=True)
    # description = models.TextField()
    # start_time = models.DateTimeField()
    # end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.id_actividad_academica.__str__() 

    # def get_absolute_url(self):
    #     return reverse("calendarapp:event-detail", args=(self.id_actividad_academica,))
    
    """Este código Django define un método get_html_url dentro de un modelo de la aplicación calendarapp. Este método utiliza el decorador @property para indicar que se trata de una propiedad calculada dinámicamente, en lugar de un campo de base de datos almacenado en la instancia del modelo.

El propósito del método get_html_url es devolver un enlace HTML que apunte a la página de detalles de un evento. En la primera línea, se utiliza la función reverse de Django para construir la URL de la página de detalles del evento, especificando el nombre de la vista event-detail y el ID del evento actual (self.id) como argumentos.

Luego, se utiliza una cadena de formato de f-string para construir la etiqueta HTML de anclaje (<a>) que incluirá el título del evento (self.title) y la URL de la página de detalles. La URL se incrusta en la cadena de formato mediante llaves ({}) y la expresión de formato {url}.

Finalmente, el método devuelve la cadena de la etiqueta HTML completa con el enlace al detalle del evento.

Este método puede ser utilizado por otros componentes de la aplicación que necesiten representar los eventos en forma de enlaces HTML. Por ejemplo, puede ser utilizado para generar enlaces de eventos en una vista de calendario o en una lista de eventos."""

    # @property
    # def get_html_url(self):
    #     url = reverse("calendarapp:event-detail", args=(self.id_actividad_academica,))
    #     return f'<a href="{url}"> {self.id_actividad_academica} </a>'
    
    class Meta:
        verbose_name_plural = "Actividades Academicas"



class DetalleActividadAcademica(models.Model):
    id_detalle_actividad_Academica= models.AutoField(primary_key=True)
    id_participante= models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='persona_participante')
    id_actividad_academica= models.ForeignKey(Event, on_delete=models.CASCADE, related_name='actividad_academica')
    # es_docente = models.BooleanField(default=False)
    # es_funcionario = models.BooleanField(default=False)
    # es_alumno = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         CheckConstraint(
    #             check=Q(es_docente=True, es_funcionario=False, es_alumno=False) |
    #                   Q(es_docente=False, es_funcionario=True, es_alumno=False) |
    #                   Q(es_docente=False, es_funcionario=False, es_alumno=True),
    #             name='unicos_participantes'
    #         )
    #     ]
    
    def toJSON(self):
        item = model_to_dict(self)
        item['value'] = self.id_participante.nombre + ' ' + self.id_participante.apellido 
        return item
    

class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    descripcion_unidad_medida= models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_unidad_medida
    
    class Meta:
        verbose_name_plural = "Unidades de Medida"

class Parametro(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    id_unidad_medida =  models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name='unidad_medida_parametro')
    descripcion_parametro = models.CharField(max_length=50, null= True)
    valor = models.IntegerField()
    es_orientacion_academica = models.BooleanField(default=False) 
    es_tutoria = models.BooleanField(default=False)
    
    class Meta:
            constraints = [
                CheckConstraint(
                    check=Q(es_tutoria=True, es_orientacion_academica=False) |
                        Q(es_tutoria=False, es_orientacion_academica=True) ,
                    name='solo_uno_puede_ser_true'
                )
            ]

            verbose_name_plural = "Parametros"
    
    def __str__(self):
        return '%s %s' % (self.descripcion_parametro, self.valor) 
        
class Cita(models.Model):
    id_cita= models.ForeignKey(Event, on_delete=models.PROTECT, related_name='ori_academ_cita', primary_key=True)
    id_parametro = models.ForeignKey(Parametro, on_delete=models.PROTECT, related_name='parametro_cita')
    es_tutoria = models.BooleanField(default=False)
    es_orientacion_academica = models.BooleanField(default=False)
    es_notificable = models.BooleanField(default=True)
    motivo= models.CharField(max_length=500, null= True)
    motivo_cancelacion = models.CharField(max_length=500, null= True)
    motivo_rechazo = models.CharField(max_length=500, null= True)
    

    class Meta:
            constraints = [
                CheckConstraint(
                    check=Q(es_tutoria=True, es_orientacion_academica=False) |
                        Q(es_tutoria=False, es_orientacion_academica=True) ,
                    name='unicos_cita'
                )
            ]
        
            verbose_name_plural = "Citas"

class TipoTutoria(models.Model):
    id_tipo_tutoria = models.AutoField(primary_key=True)
    descripcion_tipo_tutoria = models.CharField(max_length=500)

    def __str__(self):
        return self.descripcion_tipo_tutoria
    
    class Meta:
        verbose_name_plural = "Tipos de Tutoria"


class Tutoria(models.Model):
    id_tutoria = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='acri_academ_tutoria', primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, related_name='tutoria_cita', null= True)
    id_tipo_tutoria = models.ForeignKey(TipoTutoria, on_delete=models.PROTECT, related_name='tipo_tutoria')
    nombre_trabajo = models.CharField(max_length=200, null= True)

class TipoOrientacionAcademica(models.Model):
    id_tipo_orientacion_academica = models.AutoField(primary_key=True)
    descripcion_tipo_orientacion_academica = models.CharField(max_length=500)

    def __str__(self):
        return self.descripcion_tipo_orientacion_academica

    class Meta:
        verbose_name_plural = "Tutorias"

class Motivo(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    id_tipo_orientacion_academica= models.ForeignKey(TipoOrientacionAcademica, on_delete=models.SET_NULL, related_name='motivo_orientacion_academica',  null= True)
    descripcion_motivo = models.CharField(max_length=500)

    def __str__(self):
        return self.descripcion_motivo
    
    class Meta:
        verbose_name_plural = "Motivos de Orientacion Academica"

class OrientacionAcademica(models.Model):
    id_orientacion_academica = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='acti_academ_orient_academ', primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, related_name='cita_ori_academ', null= True)
    id_motivo= models.ForeignKey(Motivo, on_delete=models.PROTECT, related_name='motivo_ori_academ')
    id_tipo_orientacion_academica= models.ForeignKey(TipoOrientacionAcademica, on_delete=models.PROTECT, related_name='tipo_ori_academ')



class TipoTarea(models.Model):
    id_tipo_tarea = models.AutoField(primary_key=True)
    descripcion_tipo_tarea= models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_tipo_tarea
    
    class Meta:
        verbose_name_plural = "Tipos de tarea"

class EstadoTarea(models.Model):
    id_estado_tarea = models.AutoField(primary_key=True)
    descripcion_estado_tarea= models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion_estado_tarea
    
    class Meta:
        verbose_name_plural = "Estados de tarea"

class Tarea(models.Manager):

    id_tarea = models.AutoField(primary_key=True)
    id_tarea_relacionada = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subtarea', null=True, blank=True)
    id_funcionario_docente_finalizacion = models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, related_name='func_doc_tarea', null=True, blank=True)
    id_funcionario_docente_alta = models.ForeignKey(FuncionarioDocente, on_delete=models.PROTECT, related_name='func_doc_tarea_alta')
    id_tutoria = models.ForeignKey(Tutoria, on_delete=models.PROTECT, related_name='tarea_tutoria', null=True, blank=True)
    id_orientacion_academica = models.ForeignKey(Tutoria, on_delete=models.PROTECT, related_name='tarea_tutoria', null=True, blank=True)
    id_estado_tarea = models.ForeignKey(EstadoTarea, on_delete=models.PROTECT, related_name='tarea_estado')
    id_tipo_tarea = models.ForeignKey(TipoTarea, on_delete=models.PROTECT, related_name='tarea_estado')
    datetime_inicio =models.DateTimeField(null= True)
    datetime_vencimiento = models.DateTimeField()
    datetime_alta  =models.DateTimeField(auto_now=True)
    datetime_finalizacion = models.DateTimeField(null= True)
    datetime_ultima_modificacion = models.DateTimeField(null= True)
    observacion = models.CharField(max_length=500)
    es_notificable = models.BooleanField(default=False)


    def __str__(self):
        return self.id_tarea_relacionada
    
    class Meta:
        verbose_name_plural = "Tareas"