# Generated by Django 3.2.14 on 2023-10-16 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MateriaCarrera',
            fields=[
                ('id_materia_carrera', models.AutoField(primary_key=True, serialize=False)),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carreras_materias', to='accounts.carrera')),
                ('id_materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias_carrera', to='accounts.materia')),
            ],
            options={
                'verbose_name_plural': 'Materias Carrera',
            },
        ),
    ]