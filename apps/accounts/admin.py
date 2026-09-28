from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from apps.accounts.forms import UsuarioCreationForm
from apps.accounts.models import Usuario


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    ordering = ('email',)
    list_display = ('email', 'nombre', 'apellido', 'empresa', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'nombre', 'apellido')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Datos', {'fields': ('nombre', 'apellido', 'empresa')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'fecha_creacion')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'empresa', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('fecha_creacion', 'last_login')
