# Generated by Django 3.2.14 on 2023-05-16 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20230421_1454'),
        ('calendarapp', '0010_auto_20230516_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id_materia',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='materia', to='accounts.materia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='id_persona_receptor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persona_receptor', to='accounts.persona'),
        ),
    ]
