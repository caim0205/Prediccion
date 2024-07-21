from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.auth.hashers import make_password

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cuenta = models.OneToOneField('Cuenta', on_delete=models.CASCADE, null=True, blank=True, related_name='persona_related')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class CuentaManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Cuenta(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True, related_name='cuenta_related')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='cuentas',  # Añadir related_name para evitar conflictos
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='cuentas_permissions',  # Añadir related_name para evitar conflictos
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    objects = CuentaManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rol']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class Ciclo(models.Model):
    nombre = models.CharField(max_length=100)
    periodo_academico = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.periodo_academico}"

class Riesgo(models.Model):
    nivel = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nivel

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)  # Añadir esta línea si el estudiante pertenece a un ciclo

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.ciclo.nombre}"

class Prediccion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE)
    prediccion_actual = models.FloatField()  # Probabilidad aproximada de deserción
    riesgo_futuro = models.ForeignKey(Riesgo, on_delete=models.CASCADE)
    porcentaje_futuro = models.FloatField()  # Probabilidad en porcentaje
    prediccion_futuro = models.FloatField(default=0.0)  # Nueva columna para Predicción de Deserción con valor predeterminado
    
    def __str__(self):
        return f"Predicción para {self.estudiante} en {self.ciclo} - Riesgo Futuro: {self.riesgo_futuro} - Probabilidad Actual: {self.prediccion_actual}% - Porcentaje Futuro: {self.porcentaje_futuro}% - Predicción Futura: {self.prediccion_futuro}"
