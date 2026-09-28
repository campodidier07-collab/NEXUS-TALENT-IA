from django.conf import settings
from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    nit = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'empresa'
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

    def __str__(self):
        return self.nombre


class Area(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='areas')
    nombre = models.CharField(max_length=150)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='areas_a_cargo',
    )
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'area'
        verbose_name = 'area'
        verbose_name_plural = 'areas'
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'nombre'], name='area_unica_por_empresa'),
        ]

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='cargos')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='cargos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cargo'
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'area', 'nombre'],
                name='cargo_unico_por_area',
            ),
        ]

    def __str__(self):
        return self.nombre


class Habilidad(models.Model):
    class Categoria(models.TextChoices):
        TECNICA = 'tecnica', 'Tecnica'
        BLANDA = 'blanda', 'Blanda'
        IDIOMA = 'idioma', 'Idioma'
        OTRA = 'otra', 'Otra'

    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='habilidades')
    nombre = models.CharField(max_length=120)
    categoria = models.CharField(max_length=80, choices=Categoria.choices)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'habilidad'
        verbose_name = 'habilidad'
        verbose_name_plural = 'habilidades'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'nombre'],
                name='habilidad_unica_por_empresa',
            ),
        ]

    def __str__(self):
        return self.nombre


class CargoHabilidad(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='habilidades_requeridas')
    habilidad = models.ForeignKey(Habilidad, on_delete=models.PROTECT, related_name='cargos')
    nivel_requerido = models.PositiveSmallIntegerField(default=1)
    obligatoria = models.BooleanField(default=True)

    class Meta:
        db_table = 'cargo_habilidad'
        verbose_name = 'habilidad del cargo'
        verbose_name_plural = 'habilidades del cargo'
        constraints = [
            models.UniqueConstraint(
                fields=['cargo', 'habilidad'],
                name='habilidad_unica_por_cargo',
            ),
        ]

    def __str__(self):
        return f'{self.cargo} · {self.habilidad}'
