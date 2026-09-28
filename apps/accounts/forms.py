from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm

from apps.accounts.models import Usuario


class UsuarioCreationForm(BaseUserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'apellido', 'empresa')


class CorreoAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Correo'
        self.fields['username'].widget.attrs.update({
            'autofocus': True,
            'placeholder': 'correo@empresa.com',
        })
        self.fields['password'].label = 'Contrasena'
