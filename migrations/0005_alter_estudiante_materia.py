# Generated by Django 5.0.6 on 2024-07-11 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_estudiante_materia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante',
            name='materia',
            field=models.CharField(max_length=100),
        ),
    ]
