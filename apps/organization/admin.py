from django.contrib import admin

from apps.organization.models import Area, Cargo, CargoHabilidad, Empresa, Habilidad


class AreaInline(admin.TabularInline):
    model = Area
    extra = 0


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'correo', 'activa')
    search_fields = ('nombre', 'nit')
    inlines = [AreaInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'responsable', 'activa')
    list_filter = ('empresa', 'activa')
    search_fields = ('nombre',)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area', 'empresa', 'activo')
    list_filter = ('empresa', 'activo')
    search_fields = ('nombre',)


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'empresa', 'activa')
    list_filter = ('categoria', 'empresa', 'activa')
    search_fields = ('nombre',)


@admin.register(CargoHabilidad)
class CargoHabilidadAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'habilidad', 'nivel_requerido', 'obligatoria')
    list_filter = ('obligatoria',)
