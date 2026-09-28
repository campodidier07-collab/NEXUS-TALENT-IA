from django.conf import settings
from django.db import models

from apps.organization.models import Area, Cargo, Empresa, Habilidad


class Persona(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = 'CC', 'Cedula de ciudadania'
        CE = 'CE', 'Cedula de extranjeria'
        PAS = 'PAS', 'Pasaporte'
        PPT = 'PPT', 'Permiso por proteccion temporal'

    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='personas')
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='persona',
    )
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=20, choices=TipoDocumento.choices)
    numero_documento = models.CharField(max_length=30)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    ciudad = models.CharField(max_length=120, blank=True)
    resumen = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'persona'
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'tipo_documento', 'numero_documento'],
                name='documento_unico_por_empresa',
            ),
        ]

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class HojaVida(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PROCESADO = 'procesado', 'Procesado'
        ERROR = 'error', 'Error'

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='hojas_vida')
    archivo = models.FileField(upload_to='hojas_vida/')
    texto_extraido = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hoja_vida'
        verbose_name = 'hoja de vida'
        verbose_name_plural = 'hojas de vida'

    def __str__(self):
        return f'Hoja de vida de {self.persona}'


class Formacion(models.Model):
    class Nivel(models.TextChoices):
        TECNICO = 'tecnico', 'Tecnico'
        PREGRADO = 'pregrado', 'Pregrado'
        POSGRADO = 'posgrado', 'Posgrado'
        CURSO = 'curso', 'Curso'

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='formaciones')
    institucion = models.CharField(max_length=200)
    titulo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=40, choices=Nivel.choices)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    en_curso = models.BooleanField(default=False)

    class Meta:
        db_table = 'formacion'
        verbose_name = 'formacion'
        verbose_name_plural = 'formaciones'

    def __str__(self):
        return f'{self.titulo} · {self.institucion}'


class ExperienciaLaboral(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='experiencias')
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'experiencia_laboral'
        verbose_name = 'experiencia laboral'
        verbose_name_plural = 'experiencias laborales'

    def __str__(self):
        return f'{self.cargo} en {self.empresa}'


class PersonaHabilidad(models.Model):
    class Origen(models.TextChoices):
        MANUAL = 'manual', 'Manual'
        EXTRAIDA = 'extraida', 'Extraida'
        VALIDADA = 'validada', 'Validada'

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='habilidades')
    habilidad = models.ForeignKey(Habilidad, on_delete=models.PROTECT, related_name='personas')
    nivel = models.PositiveSmallIntegerField(default=1)
    origen = models.CharField(max_length=20, choices=Origen.choices, default=Origen.MANUAL)

    class Meta:
        db_table = 'persona_habilidad'
        verbose_name = 'habilidad de la persona'
        verbose_name_plural = 'habilidades de la persona'
        constraints = [
            models.UniqueConstraint(
                fields=['persona', 'habilidad'],
                name='habilidad_unica_por_persona',
            ),
        ]

    def __str__(self):
        return f'{self.persona} · {self.habilidad}'


class Empleado(models.Model):
    class TipoContrato(models.TextChoices):
        INDEFINIDO = 'indefinido', 'Indefinido'
        FIJO = 'fijo', 'Fijo'
        PRESTACION = 'prestacion', 'Prestacion de servicios'
        APRENDIZAJE = 'aprendizaje', 'Aprendizaje'

    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        INACTIVO = 'inactivo', 'Inactivo'

    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, related_name='empleado')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='empleados')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='empleados')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='empleados')
    fecha_ingreso = models.DateField()
    fecha_retiro = models.DateField(null=True, blank=True)
    tipo_contrato = models.CharField(max_length=40, choices=TipoContrato.choices)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = 'empleado'
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'

    def __str__(self):
        return str(self.persona)
