from django.contrib import admin

from apps.recruitment.models import AnalisisIA, Entrevista, HistorialPostulacion, Postulacion, Vacante


class HistorialInline(admin.TabularInline):
    model = HistorialPostulacion
    extra = 0


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cargo', 'area', 'estado', 'modalidad', 'empresa')
    list_filter = ('estado', 'modalidad', 'empresa')
    search_fields = ('titulo',)


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'vacante', 'estado', 'compatibilidad', 'fecha_postulacion')
    list_filter = ('estado',)
    search_fields = ('persona__nombres', 'persona__apellidos', 'vacante__titulo')
    inlines = [HistorialInline]


@admin.register(Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display = ('postulacion', 'entrevistador', 'fecha', 'resultado')


@admin.register(AnalisisIA)
class AnalisisIAAdmin(admin.ModelAdmin):
    list_display = ('postulacion', 'tipo', 'modelo', 'fecha')
