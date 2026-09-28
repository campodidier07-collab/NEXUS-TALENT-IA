from django.contrib import admin

from apps.auditoria.models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'tabla', 'registro_id')
    list_filter = ('accion', 'tabla')
    search_fields = ('accion', 'detalle')
    readonly_fields = ('usuario', 'accion', 'tabla', 'registro_id', 'detalle', 'direccion_ip', 'fecha')
