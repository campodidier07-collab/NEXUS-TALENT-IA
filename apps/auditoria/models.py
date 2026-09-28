from django.conf import settings
from django.db import models


class Auditoria(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='auditorias',
    )
    accion = models.CharField(max_length=80)
    tabla = models.CharField(max_length=80)
    registro_id = models.BigIntegerField(null=True, blank=True)
    detalle = models.TextField(blank=True)
    direccion_ip = models.CharField(max_length=45, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auditoria'
        verbose_name = 'auditoria'
        verbose_name_plural = 'auditorias'

    def __str__(self):
        return f'{self.accion} · {self.tabla}'
