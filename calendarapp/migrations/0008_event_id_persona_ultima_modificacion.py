# Generated by Django 3.2.14 on 2023-09-05 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_post_timestamp'),
        ('calendarapp', '0007_tarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='id_persona_ultima_modificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evento_modificacion', to='accounts.persona'),
        ),
    ]