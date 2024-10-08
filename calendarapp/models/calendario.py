from django.db import models
from django.forms import ValidationError, model_to_dict
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from accounts.models.user import FuncionarioDocente

from calendarapp.models import EventAbstract
from accounts.models import User


class Dia(models.Model):
    id_dia= models.AutoField(primary_key=True)
    descripcion_dia = models.CharField(max_length=15, unique= True, null= False)

    def __str__(self):
        return '%s' % (self.descripcion_dia)
    
    class Meta:
        verbose_name_plural = "Dias"


class Semestre(models.Model):
    id_semestre= models.AutoField(primary_key=True)
    descripcion_semestre = models.CharField(max_length=15, unique= True, null= False)

    def __str__(self):
        return '%s' % (self.descripcion_semestre)
    
    class Meta:
        verbose_name_plural = "Semestres"
    
class Convocatoria(models.Model):
    id_convocatoria= models.AutoField(primary_key=True)
    id_semestre= models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='semestre_calendario')
    anho= models.IntegerField(validators=[MinValueValidator(datetime.now().year)])
    fecha_inicio= models.DateField()
    fecha_fin= models.DateField()

    def clean(self):
        if self.anho != datetime.now().year:
            raise ValidationError('El año ingresado debe ser el año actual.')
    
    def __str__(self):
        return '%s %s' % (self.id_semestre.descripcion_semestre, self.anho)
    
    class Meta:
        verbose_name_plural = "Convocatorias"

class HorarioSemestral(models.Model):
    id_horario_semestral= models.AutoField(primary_key=True)
    id_funcionario_docente= models.ForeignKey(FuncionarioDocente, on_delete=models.CASCADE, related_name='func_doc_calendario')
    id_convocatoria= models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='convocatoria_calendario')
    id_dia= models.ForeignKey(Dia, on_delete=models.CASCADE, related_name='hsem_dia')
    hora_inicio= models.TimeField()
    hora_fin= models.TimeField()

    class Meta:
        verbose_name_plural = "Horarios Semestrales"
        
        
    def toJSON(self):
        item = model_to_dict(self)
        return item


    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['id_funcionario_docente', 'id_convocatoria', 'id_dia', 'hora_inicio', 'hora_fin'], name='unique_horario_semestral') # violation_error_message='El rango de horas cargadas deben ser únicos para el mismo funcionario/docente en el mismo dia y convocatoria.'),
    #     ]

    # class Meta:
    #     unique_together =['id_funcionario_docente', 'id_convocatoria', 'id_dia', 'hora_inicio', 'hora_fin']

    # def __str__(self):
    #         return '%s %s %s %s %s %s %s' % (self.id_horario_semestral, self.id_funcionario_docente, self.id_convocatoria.id_semestre.descripcion_semestre, self.id_convocatoria.anho , self.id_dia.descripcion_dia, self.hora_fin, self.hora_fin)