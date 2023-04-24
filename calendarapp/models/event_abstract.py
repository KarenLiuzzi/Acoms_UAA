from django.db import models



class EventAbstract(models.Model):
    """ Event abstract model """

    id_actividad_academica= models.AutoField(primary_key=True)

    # is_active = models.BooleanField(default=True)
    # is_deleted = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
