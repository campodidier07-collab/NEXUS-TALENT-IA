from django.conf import settings
from django.db import models

from apps.organization.models import Area, Cargo, Empresa
from apps.people.models import Persona


class Vacante(models.Model):
    class Modalidad(models.TextChoices):
        PRESENCIAL = 'presencial', 'Presencial'
        REMOTO = 'remoto', 'Remoto'
        HIBRIDO = 'hibrido', 'Hibrido'

    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADA = 'publicada', 'Publicada'
        CERRADA = 'cerrada', 'Cerrada'
        CANCELADA = 'cancelada', 'Cancelada'

    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='vacantes')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='vacantes')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='vacantes')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    modalidad = models.CharField(max_length=20, choices=Modalidad.choices)
    ubicacion = models.CharField(max_length=150, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='vacantes_creadas',
    )
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vacante'
        verbose_name = 'vacante'
        verbose_name_plural = 'vacantes'

    def __str__(self):
        return self.titulo


class Postulacion(models.Model):
    class Estado(models.TextChoices):
        RECIBIDA = 'recibida', 'Recibida'
        EN_REVISION = 'en_revision', 'En revisión'
        ENTREVISTA = 'entrevista', 'Entrevista'
        PRUEBA = 'prueba', 'Prueba'
        SELECCIONADA = 'seleccionada', 'Seleccionada'
        DESCARTADA = 'descartada', 'Descartada'
        CONTRATADA = 'contratada', 'Contratada'

    vacante = models.ForeignKey(Vacante, on_delete=models.PROTECT, related_name='postulaciones')
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='postulaciones')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.RECIBIDA)
    compatibilidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    explicacion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    actualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='postulaciones_actualizadas',
    )

    class Meta:
        db_table = 'postulacion'
        verbose_name = 'postulacion'
        verbose_name_plural = 'postulaciones'
        constraints = [
            models.UniqueConstraint(
                fields=['vacante', 'persona'],
                name='postulacion_unica',
            ),
        ]

    def __str__(self):
        return f'{self.persona} · {self.vacante}'


class HistorialPostulacion(models.Model):
    postulacion = models.ForeignKey(
        Postulacion,
        on_delete=models.CASCADE,
        related_name='historial',
    )
    estado_anterior = models.CharField(max_length=20, blank=True)
    estado_nuevo = models.CharField(max_length=20)
    comentario = models.TextField(blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cambios_de_postulacion',
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_postulacion'
        verbose_name = 'historial de postulacion'
        verbose_name_plural = 'historial de postulaciones'

    def __str__(self):
        return f'{self.estado_anterior or "inicio"} -> {self.estado_nuevo}'


class Entrevista(models.Model):
    class Resultado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        CONTINUA = 'continua', 'Continua'
        NO_CONTINUA = 'no_continua', 'No continua'

    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='entrevistas')
    entrevistador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='entrevistas',
    )
    fecha = models.DateTimeField()
    resultado = models.CharField(
        max_length=20,
        choices=Resultado.choices,
        default=Resultado.PENDIENTE,
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = 'entrevista'
        verbose_name = 'entrevista'
        verbose_name_plural = 'entrevistas'

    def __str__(self):
        return f'Entrevista {self.fecha:%Y-%m-%d}'


class AnalisisIA(models.Model):
    class Tipo(models.TextChoices):
        EXTRACCION = 'extraccion', 'Extraccion'
        COMPATIBILIDAD = 'compatibilidad', 'Compatibilidad'
        PREGUNTAS = 'preguntas', 'Preguntas'

    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='analisis')
    tipo = models.CharField(max_length=40, choices=Tipo.choices)
    modelo = models.CharField(max_length=80)
    resultado = models.JSONField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analisis_ia'
        verbose_name = 'analisis de IA'
        verbose_name_plural = 'analisis de IA'

    def __str__(self):
        return f'{self.get_tipo_display()} · {self.postulacion}'
