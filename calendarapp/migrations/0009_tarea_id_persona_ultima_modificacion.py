# Generated by Django 3.2.14 on 2023-09-05 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_post_timestamp'),
        ('calendarapp', '0008_event_id_persona_ultima_modificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='id_persona_ultima_modificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tarea_modificacion', to='accounts.persona'),
        ),
    ]
