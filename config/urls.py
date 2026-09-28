from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.accounts.forms import CorreoAuthenticationForm
from apps.dashboard.views import inicio

admin.site.site_header = 'NEXUS Talent IA'
admin.site.site_title = 'NEXUS'
admin.site.index_title = 'Administración'

urlpatterns = [
    path('', inicio, name='inicio'),
    path(
        'cuentas/ingresar/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=CorreoAuthenticationForm,
        ),
        name='login',
    ),
    path('cuentas/salir/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'cuentas/recuperar/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.txt',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'cuentas/recuperar/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'cuentas/recuperar/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'cuentas/recuperar/listo/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
