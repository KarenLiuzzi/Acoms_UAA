# Generated by Django 3.2.14 on 2023-03-28 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_auto_20230314_2058'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='horariosemestral',
            name='unique_horario_semestral',
        ),
    ]