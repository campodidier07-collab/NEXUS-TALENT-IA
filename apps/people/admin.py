from django.contrib import admin

from apps.people.models import (
    Empleado,
    ExperienciaLaboral,
    Formacion,
    HojaVida,
    Persona,
    PersonaHabilidad,
)


class HojaVidaInline(admin.TabularInline):
    model = HojaVida
    extra = 0


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'correo', 'empresa')
    list_filter = ('empresa', 'tipo_documento', 'activo')
    search_fields = ('nombres', 'apellidos', 'numero_documento', 'correo')
    inlines = [HojaVidaInline]


@admin.register(Formacion)
class FormacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'nivel', 'persona')
    search_fields = ('titulo', 'institucion')


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'persona', 'actualmente')
    search_fields = ('cargo', 'empresa')


@admin.register(PersonaHabilidad)
class PersonaHabilidadAdmin(admin.ModelAdmin):
    list_display = ('persona', 'habilidad', 'nivel', 'origen')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'cargo', 'area', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'empresa')
