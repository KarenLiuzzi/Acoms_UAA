# Generated by Django 3.2.14 on 2023-11-10 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_materiacarrera'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionariodocente',
            name='id_facultad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facultad_funcionario_docente', to='accounts.facultad'),
        ),
        migrations.AddConstraint(
            model_name='funcionariodocente',
            constraint=models.CheckConstraint(check=models.Q(('id_departamento__isnull', False), ('id_facultad__isnull', False), _negated=True), name='departamento_facultad_constraint'),
        ),
    ]
