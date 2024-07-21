from django.db import migrations

def create_initial_roles(apps, schema_editor):
    Rol = apps.get_model('my_app', 'Rol')
    Rol.objects.create(nombre='admin', descripcion='Acceso a todo el sistema')
    Rol.objects.create(nombre='secretaria', descripcion='Generar predicciones y registrar usuarios')
    Rol.objects.create(nombre='docente', descripcion='Generar predicciones y recibe informes')

class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),  # Asegúrate de que esta sea la migración inicial correcta
    ]

    operations = [
        migrations.RunPython(create_initial_roles),
    ]
