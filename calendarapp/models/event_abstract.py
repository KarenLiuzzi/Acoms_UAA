from django.db import models



class EventAbstract(models.Model):
    """ Event abstract model """

    id_actividad_academica= models.AutoField(primary_key=True)

    class Meta:
        abstract = True
