from django.db import models
from django.db.models import F
from django.forms import model_to_dict
from calendarapp.models import EventAbstract
from django.db.models import Q, CheckConstraint
from itertools import chain
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import os

"""models.Manager es una clase de Django que proporciona un mecanismo para realizar consultas a la base de datos y realizar operaciones en los modelos de manera más fácil y eficiente. Cada modelo de Django tiene al menos un objeto Manager asociado a él de forma predeterminada.

Los objetos Manager de los modelos de Django son responsables de proporcionar un conjunto de métodos para interactuar con la base de datos. Por ejemplo, objects.all() devuelve todos los registros de la base de datos para un modelo específico, mientras que objects.filter() permite realizar consultas más avanzadas para recuperar un subconjunto específico de registros.

También puedes crear tus propios objetos Manager personalizados para extender las funcionalidades por defecto y ajustar las consultas a tus necesidades específicas.

En resumen, models.Manager es un componente clave de Django que proporciona una API de consulta a la base de datos para modelos de Django, y permite interactuar de manera eficiente y efectiva con la información almacenada en la base de datos."""


class EventManager(models.Manager):
    """ Event manager. select_related: Sin embargo, debes tener en cuenta que esta optimización solo funciona para relaciones ForeignKey y OneToOneField. Si estás trabajando con relaciones ManyToManyField, deberás utilizar el método prefetch_related para optimizar las consultas. """

    def get_all_events(self):
        
        events = Cita.objects.select_related("id_cita")

        return events
    """como hacer un inner join con dos modelos y obtener columnas seleccionadas con filtros especificos en django"""
    
    def get_all_acti_academ(self):
        
        tutorias = Tutoria.objects.select_related("id_tutoria").annotate(id_actividad_academica=F("id_tutoria")).filter(id_cita= None)
        orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").annotate(id_actividad_academica=F("id_orientacion_academica")).filter(id_cita= None)
        
        # Combinar los dos querysets en una sola variable
        events= list(chain(tutorias, orientaciones))

        return events
    
    def get_all_actividades(self):
        #actividades con citas
        citas = Cita.objects.select_related("id_cita")
        #tutorias sin citas
        tutorias = Tutoria.objects.select_related("id_tutoria").filter(id_cita= None)
        #orientaciones sin citas
        orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").filter(id_cita= None)

        # Combinar los dos querysets en una sola variable
        all_events= list(chain(citas, tutorias, orientaciones))

        return all_events

    #este usamos para traer un solo tipo de cita, ya sea de tipo tutoria u orientacion academica 
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
    
    def get_running_acti_academ(self, tipo_cita):
        if tipo_cita == 'Tutoria':
            running_events = Tutoria.objects.select_related("id_tutoria").annotate(id_actividad_academica=F("id_tutoria")).filter(id_cita= None)
            
        elif tipo_cita== "OriAcademica":
            running_events = OrientacionAcademica.objects.select_related("id_orientacion_academica").annotate(id_actividad_academica=F("id_orientacion_academica")).filter(id_cita= None)
        else: 
            tutorias = Tutoria.objects.select_related("id_tutoria").annotate(id_actividad_academica=F("id_tutoria")).filter(id_cita= None)
            orientaciones = OrientacionAcademica.objects.select_related("id_orientacion_academica").annotate(id_actividad_academica=F("id_orientacion_academica")).filter(id_cita= None)
            running_events = list(chain(tutorias, orientaciones))

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

    id_estado_actividad_academica= models.ForeignKey(EstadoActividadAcademica, on_delete=models.CASCADE, related_name='estado_acti_aca')
    id_convocatoria= models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='convocatoria')
    id_facultad= models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='facultad')
    id_materia= models.ForeignKey(Materia, on_delete=models.CASCADE, blank=True, null=True)
    id_departamento= models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='departamento', blank=True, null=True)
    id_funcionario_docente_encargado= models.ForeignKey(FuncionarioDocente, on_delete=models.CASCADE, related_name='funcionario_docente_encarcado')
    id_persona_solicitante= models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True)
    id_persona_alta= models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='persona_alta')
    datetime_inicio_estimado = models.DateTimeField()
    datetime_fin_estimado = models.DateTimeField()
    datetime_inicio_real = models.DateTimeField(null= True, blank=True)
    datetime_fin_real = models.DateTimeField(null= True, blank=True)
    datetime_registro = models.DateTimeField() #auto_now=True
    observacion= models.CharField(max_length=500, null= True, blank=True)
    nro_curso= models.CharField(max_length=30, null= True, blank=True)
    id_persona_ultima_modificacion= models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True, related_name='evento_modificacion')

    objects = EventManager()

    def __str__(self):
        return self.id_actividad_academica.__str__() 
    class Meta:
        verbose_name_plural = "Actividades Academicas"
        #permisos personalizados
        permissions= [('iniciar_cita', 'Iniciar cita'), ('finalizar_cita', 'Finalizar cita' ), ('editar_cita', 'Editar cita'), ('cancelar_cita', 'Cancelar cita'), ('confirmar_cita', 'Confirmar cita'), ('registrar_cita', 'registar cita'),('rechazar_cita', 'rechazar cita'), ('editar_actividad_academica', 'Editar Actividad Academica'), ('registrar_actividad_academica', 'Registrar Actividad Academica'), ('cancelar_actividad_academica', 'Cancelar Actividad Academica'), ('finalizar_actividad_academica', 'Finalizar Actividad Academica')]

class DetalleActividadAcademica(models.Model):
    id_detalle_actividad_Academica= models.AutoField(primary_key=True)
    id_participante= models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='persona_participante')
    id_actividad_academica= models.ForeignKey(Event, on_delete=models.CASCADE, related_name='actividad_academica')
    
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
    id_unidad_medida =  models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, related_name='unidad_medida_parametro')
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
    id_cita= models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ori_academ_cita', primary_key=True)
    id_parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='parametro_cita')
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
    id_tutoria = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='acri_academ_tutoria', primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='tutoria_cita', null= True)
    id_tipo_tutoria = models.ForeignKey(TipoTutoria, on_delete=models.CASCADE, related_name='tipo_tutoria')
    nombre_trabajo = models.CharField(max_length=200, null= True)
    motivo_cancelacion = models.CharField(max_length=500, null= True)
    
class TipoOrientacionAcademica(models.Model):
    id_tipo_orientacion_academica = models.AutoField(primary_key=True)
    descripcion_tipo_orientacion_academica = models.CharField(max_length=500)

    def __str__(self):
        return self.descripcion_tipo_orientacion_academica

    class Meta:
        verbose_name_plural = "Tipos de orientacion academica"

class Motivo(models.Model):
    id_motivo = models.AutoField(primary_key=True)
    id_tipo_orientacion_academica= models.ForeignKey(TipoOrientacionAcademica, on_delete=models.CASCADE, related_name='motivo_orientacion_academica',  null= True)
    descripcion_motivo = models.CharField(max_length=500)

    def __str__(self):
        return self.descripcion_motivo
    
    class Meta:
        verbose_name_plural = "Motivos de Orientacion Academica"

class OrientacionAcademica(models.Model):
    id_orientacion_academica = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='acti_academ_orient_academ', primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='cita_ori_academ', null= True)
    id_motivo= models.ForeignKey(Motivo, on_delete=models.CASCADE, related_name='motivo_ori_academ')
    id_tipo_orientacion_academica= models.ForeignKey(TipoOrientacionAcademica, on_delete=models.CASCADE, related_name='tipo_ori_academ')
    motivo_cancelacion = models.CharField(max_length=500, null= True)


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

class Tarea(models.Model):

    id_tarea = models.AutoField(primary_key=True)
    id_persona_finalizacion = models.ForeignKey(Persona,  related_name='persona_tarea_finalizacion', on_delete=models.CASCADE, null= True)
    id_persona_alta = models.ForeignKey(Persona, related_name='persona_tarea_alta', on_delete=models.CASCADE, null= True)
    id_persona_responsable = models.ForeignKey(Persona, related_name='persona_tarea_responsalbe', on_delete=models.CASCADE, null= True)
    id_tutoria = models.ForeignKey(Tutoria, related_name='tarea_tutoria', on_delete=models.CASCADE, null= True)
    id_orientacion_academica = models.ForeignKey(OrientacionAcademica, related_name='tarea_ori_academ', on_delete=models.CASCADE, null= True)
    id_estado_tarea = models.ForeignKey(EstadoTarea, on_delete=models.CASCADE, related_name='tarea_estado')
    id_tipo_tarea = models.ForeignKey(TipoTarea, on_delete=models.CASCADE, related_name='tarea_tipo')
    datetime_inicio_estimado = models.DateTimeField(null= True)
    datetime_inicio_real = models.DateTimeField(null= True)
    datetime_vencimiento = models.DateTimeField(null= True)
    datetime_alta = models.DateTimeField()
    datetime_finalizacion = models.DateTimeField(null= True)
    datetime_ultima_modificacion = models.DateTimeField(auto_now=True)
    observacion = models.CharField(max_length=500)
    es_notificable = models.BooleanField(default=True)
    id_persona_ultima_modificacion= models.ForeignKey(Persona, on_delete=models.CASCADE, blank=True, null=True, related_name='tarea_modificacion')

    class Meta:
        verbose_name_plural = "Tareas"
        
        
#aqui construimos nuestros singals
from django.db.models.signals import post_save, pre_save
from notify.signals import notificar

def notify_cita(sender, instance, created, **kwargs):

    try:
        #para que notifique una sola vez
        if created:
            
            title= 'Nueva solicitud de cita'
            #traemos del user del solicitante
            ins_solicitante= Persona.objects.get(id= instance.id_cita.id_persona_solicitante.id)
            ins_encargado= Persona.objects.get(id= instance.id_cita.id_funcionario_docente_encargado.id_funcionario_docente.id)
            
            tipo_cita= ''
            if instance.es_tutoria== True:
                tipo_cita= 'cita_tutoria'
            elif instance.es_orientacion_academica== True:
                tipo_cita= 'cita_orientacion'
            else:
                tipo_cita= ''
                
            solicitante= ins_solicitante.usuario.all().first()
            encargado = ins_encargado.usuario.all().first()
            id_actividad= instance.id_cita.id_actividad_academica

            notificar.send(solicitante, destiny= encargado, verb= title, level='info', tipo= tipo_cita , id_tipo= id_actividad)
            # enviar_notificacion_a_usuario(encargado.id, 'notificar')
            
    except Exception as e:
        print(f"Se ha producido un error: {e}")
    
post_save.connect(notify_cita, sender= Cita)

#cambia el estado de Event 
def detectar_cambio_estado(sender, instance, **kwargs):
    
    try:
        if instance.id_actividad_academica:
            original_instance = sender.objects.get(id_actividad_academica=instance.id_actividad_academica)
            
            # Comprueba si el campo id_estado_actividad_academica ha cambiado
            if original_instance.id_estado_actividad_academica != instance.id_estado_actividad_academica:
                
                #traemos del user del solicitante
                ins_solicitante= Persona.objects.filter(id= instance.id_persona_solicitante.id).first()
                ins_encargado= Persona.objects.filter(id= instance.id_funcionario_docente_encargado.id_funcionario_docente.id).first()

                id_actividad= instance.id_actividad_academica
                destino= ''
                contenido= ''
                tipo= ''
                nombre_actividad= ''
                title= ''
                
                #Verificamos de que tipo de actividad academica corresponde
                cita_existente = Cita.objects.filter(id_cita=id_actividad).first()
                tutoria_existente = Tutoria.objects.filter(id_tutoria=id_actividad).first()
                orientacion_existente = OrientacionAcademica.objects.filter(id_orientacion_academica=id_actividad).first()
                
                if cita_existente is not None:
                    if cita_existente.es_tutoria == True:
                        tipo= 'cita_tutoria'
                        nombre_actividad= 'Cita de Tutoría'
                    else:
                        tipo= 'cita_orientacion'
                        nombre_actividad= 'Cita de Orientación Académica'
                        
                elif tutoria_existente is not None:
                    tipo= 'tutoria'
                    nombre_actividad= 'Tutoría'
                    
                elif orientacion_existente is not None:
                    tipo= 'orientacion'
                    nombre_actividad= 'Orientación Académica'
                
                #preguntamos si es que la persona que modifico es igual al solicitante entonces enviar al encargado
                if instance.id_persona_ultima_modificacion == instance.id_persona_solicitante:
                    originador= ins_solicitante.usuario.all().first()
                    destinatario = ins_encargado.usuario.all().first()
                    if destinatario is not None:
                        destino= destinatario.email
                    else:
                        destino= None
                    
                    if instance.id_estado_actividad_academica.descripcion_estado_actividad_academica == 'Cancelada':
                        title = nombre_actividad + ' cancelada.'
                        
                        if (tipo== 'cita_tutoria' or  tipo== 'cita_orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue cancelada.  Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
                    
                #preguntamos si es que la persona que modifico es igual al encargado entonces enviar al solicitante
                elif instance.id_persona_ultima_modificacion.id == instance.id_funcionario_docente_encargado.id_funcionario_docente.id:
                    originador= ins_encargado.usuario.all().first()
                    destinatario = ins_solicitante.usuario.all().first()
                    if destinatario is not None:
                        destino= destinatario.email
                    else:
                        destino= None
                        
                    if instance.id_estado_actividad_academica.descripcion_estado_actividad_academica == 'Cancelada':
                        title = nombre_actividad + ' cancelada.'
                        
                        if (tipo== 'cita_tutoria' or  tipo== 'cita_orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue cancelada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)

                        if (tipo== 'tutoria' or  tipo== 'orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue finalizada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
                    
                    elif instance.id_estado_actividad_academica.descripcion_estado_actividad_academica == 'Confirmada':
                        title = nombre_actividad + ' confirmada.'
                        
                        if (tipo== 'cita_tutoria' or  tipo== 'cita_orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue confirmada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
                            
                    elif instance.id_estado_actividad_academica.descripcion_estado_actividad_academica == 'Rechazada':
                        title = nombre_actividad + ' rechazada.'
                        
                        if (tipo== 'cita_tutoria' or  tipo== 'cita_orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue rechazada. Puede verificar el mismo ingresando al portal web.Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
                        
                    elif instance.id_estado_actividad_academica.descripcion_estado_actividad_academica == 'Finalizada':
                        title = nombre_actividad + ' finalizada.'
                        
                        if (tipo== 'tutoria' or  tipo== 'orientacion'):
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue finalizada. Puede verificar el mismo ingresando al portal web.Atte equipo AcOms.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
    
    except Exception as e:
        print(f"Se ha producido un error: {e}")
        
pre_save.connect(detectar_cambio_estado, sender= Event)

#notificar tarea
def notify_tarea(sender, instance, created, **kwargs):
    
    try:
        #para que notifique una sola vez
        if created:
            if (instance.id_estado_tarea.descripcion_estado_tarea == 'Pendiente' or instance.id_estado_tarea.descripcion_estado_tarea == 'Iniciada'):
                tipo_actividad= ''
                id_actividad=''
                title= ''
                cita_existente_tutoria= None
                cita_existente_orrientacion= None
                
                #traemos del user del solicitante
                ins_solicitante= Persona.objects.filter(id= instance.id_persona_alta.id).first()
                #agregamos
                ins_encargado= Persona.objects.filter(id= instance.id_persona_responsable.id).first()
                
                #preguntamos si la persona solicitante es diferente de la encargada entonces no notificar
                if ins_solicitante != ins_encargado :
                
                    #Verificamos si existe una cita relacionada
                    if instance.id_tutoria is not None:
                        cita_existente_tutoria = Cita.objects.filter(id_cita=instance.id_tutoria.id_tutoria.id_actividad_academica).first()
                    elif instance.id_orientacion_academica is not None:
                        cita_existente_orrientacion = Cita.objects.filter(id_cita=instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica).first()
                    
                    
                    if cita_existente_tutoria is not None:
                        tipo_actividad= 'tarea_cita_tutoria'
                        id_actividad= instance.id_tutoria.id_tutoria.id_actividad_academica
                        title = 'Te asignaron una tarea en una cita de tutoría'
                            
                    elif cita_existente_orrientacion is not None:
                        id_actividad= instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                        tipo_actividad= 'tarea_cita_orientacion'            
                        title = 'Te asignaron una tarea en una cita de orientación académica'
                        
                    elif instance.id_tutoria != None:
                        id_actividad= instance.id_tutoria.id_tutoria.id_actividad_academica
                        tipo_actividad= 'tarea_tutoria'            
                        title = 'Te asignaron una tarea en una tutoría'
                        
                    elif instance.id_orientacion_academica != None:
                        id_actividad= instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                        tipo_actividad= 'tarea_orientacion'
                        title = 'Te asignaron una tarea en una orientación académica'
                    
                    solicitante= ins_solicitante.usuario.all().first()
                    encargado = ins_encargado.usuario.all().first()

                    notificar.send(solicitante, destiny= encargado, verb= title, level='info', tipo= tipo_actividad , id_tipo= id_actividad)

    except Exception as e:
        print(f"Se ha producido un error: {e}")
    
post_save.connect(notify_tarea, sender= Tarea)

# #cambia el estado de Tarea
def detectar_cambio_estado_tarea(sender, instance, **kwargs):
    
    try:
        if instance.id_tarea:
            original_instance = sender.objects.get(id_tarea=instance.id_tarea)
            
            # Comprueba si el campo id_estado_actividad_academica ha cambiado
            if original_instance.id_estado_tarea != instance.id_estado_tarea:
                
                #traemos del user del solicitante
                ins_solicitante= Persona.objects.filter(id= instance.id_persona_alta.id).first()
                tipo= ''
                nombre_actividad= ''
                title= ''
                id_actividad= ''
                cita_existente_tutoria= None
                cita_existente_orrientacion= None
                
                #preguntamos si es que la persona que modifico es diferente de la solicitante avisar al solicitante
                if instance.id_persona_ultima_modificacion !=  instance.id_persona_alta:
                
                    #Verificamos si existe una cita relacionada
                    if instance.id_tutoria is not None:
                        cita_existente_tutoria = Cita.objects.filter(id_cita=instance.id_tutoria.id_tutoria.id_actividad_academica).first()
                    elif instance.id_orientacion_academica is not None:
                        cita_existente_orrientacion = Cita.objects.filter(id_cita=instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica).first()
                    
                    if cita_existente_tutoria is not None:
                        print('entro en cita tutoria')
                        tipo= 'tarea_cita_tutoria'
                        nombre_actividad= 'Tarea de cita de Tutoría'
                        id_actividad= instance.id_tutoria.id_tutoria.id_actividad_academica
                            
                    elif cita_existente_orrientacion is not None:
                        print('entro en cita orientacion')
                        id_actividad= instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                        tipo= 'tarea_cita_orientacion'
                        nombre_actividad= 'Tarea de cita de Orientación Académica'
                            
                    elif instance.id_tutoria != None:
                        print('entro en tutoria')
                        id_actividad= instance.id_tutoria.id_tutoria.id_actividad_academica
                        tipo= 'tarea_tutoria'
                        nombre_actividad= 'Tarea de Tutoría'
                        
                    elif instance.id_orientacion_academica != None:
                        print('entro en orientacion')
                        id_actividad= instance.id_orientacion_academica.id_orientacion_academica.id_actividad_academica
                        tipo= 'tarea_orientacion'
                        nombre_actividad= 'Tarea de Orientación Académica'    
                
                    ins_persona_modificacion= Persona.objects.get(id= instance.id_persona_ultima_modificacion.id)
                    originador= ins_persona_modificacion.usuario.all().first()
                    destino= ''
                    destinatario = ins_solicitante.usuario.all().first()
                    if destinatario is not None:
                        destino= destinatario.email
                    
                        if instance.id_estado_tarea.descripcion_estado_tarea == 'Cancelada':
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue cancelada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            title = nombre_actividad + ' cancelada.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
                        
                        elif instance.id_estado_tarea.descripcion_estado_tarea == 'Iniciada':
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue iniciada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            title = nombre_actividad + ' iniciada.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)                    
                            
                        elif instance.id_estado_tarea.descripcion_estado_tarea == 'Finalizada':
                            contenido= f'Estimad@: Le informamos que su "{nombre_actividad}" fue finalizada. Puede verificar el mismo ingresando al portal web. Atte equipo AcOms.'
                            title = nombre_actividad + ' finalizada.'
                            enviarcorreo(title, contenido, destino)
                            notificar.send(originador, destiny= destinatario, verb= title, level='info', tipo= tipo , id_tipo= id_actividad)
            
    except Exception as e:
        print(f"Se ha producido un error en notficiar tarea: {e}")
        
pre_save.connect(detectar_cambio_estado_tarea, sender= Tarea)

#configurar el setting.py, crear logica de envio de correo, obtener el mail del token
# def enviarcorreo(asunto, contenido, destinatario):
#     message= Mail(
#         from_email= 'beatrizmoon@hotmail.com' ,
#         to_emails= destinatario,
#         subject= asunto,
#         html_content= contenido
#     )

#     try:
#         #si es necesario hacer la obtencion del token con una variable global 
#         sg= SendGridAPIClient(os.environ.get('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'))
#         response = sg.send(message)
#     except Exception as e:
#         pass
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviarcorreo(asunto, contenido, destinatario):
    
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

    # Inicia sesión en tu cuenta de Gmail
    server.login(sender_email, sender_password)

    # Crea el mensaje de correo
    subject = asunto
    body = contenido
    recipient_email = destinatario

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Envía el correo
        server.sendmail(sender_email, recipient_email, msg.as_string())
        # Cierra la conexión SMTP
        server.quit()
        print('Correo enviado con éxito')
    except Exception as e:
        print(f"Se ha producido un error: {e}")
        
