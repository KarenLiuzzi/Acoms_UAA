# Generated by Django 3.2.14 on 2023-05-16 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0009_auto_20230516_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='datetime_fin_real',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime_inicio_real',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
