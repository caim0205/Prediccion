from django.db import migrations

def add_roles(apps, schema_editor):
    Rol = apps.get_model('my_app', 'Rol')
    Rol.objects.get_or_create(nombre='admin', descripcion='Acceso a todo el sistema')
    Rol.objects.get_or_create(nombre='secretaria', descripcion='Generar predicciones y registrar usuarios')
    Rol.objects.get_or_create(nombre='docente', descripcion='Generar predicciones y recibe informes')

class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0015_merge_20240721_0442'),  # Asegúrate de que este nombre coincida con la última migración
    ]

    operations = [
        migrations.RunPython(add_roles),
    ]

