from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from apps.organization.models import Area, Cargo
from apps.people.models import Empleado, Persona
from apps.recruitment.models import Postulacion, Vacante


def _saludo():
    hora = timezone.localtime().hour
    if hora < 12:
        return 'Buenos días'
    if hora < 19:
        return 'Buenas tardes'
    return 'Buenas noches'


def _por_empresa(queryset, empresa_id, campo='empresa_id'):
    if empresa_id:
        return queryset.filter(**{campo: empresa_id})
    return queryset


def portada(request):
    return render(request, 'landing/portada.html')


@login_required
def inicio(request):
    empresa = request.user.empresa
    empresa_id = request.user.empresa_id

    vacantes = _por_empresa(Vacante.objects.all(), empresa_id)
    personas = _por_empresa(Persona.objects.all(), empresa_id)
    postulaciones = _por_empresa(
        Postulacion.objects.all(),
        empresa_id,
        'vacante__empresa_id',
    )
    empleados = _por_empresa(Empleado.objects.all(), empresa_id)
    areas = _por_empresa(Area.objects.all(), empresa_id)
    cargos = _por_empresa(Cargo.objects.all(), empresa_id)

    conteo_estados = {
        fila['estado']: fila['total']
        for fila in postulaciones.values('estado').annotate(total=Count('id'))
    }
    pipeline = [
        {
            'codigo': codigo,
            'nombre': etiqueta,
            'total': conteo_estados.get(codigo, 0),
        }
        for codigo, etiqueta in Postulacion.Estado.choices
    ]
    mayor = max((paso['total'] for paso in pipeline), default=0)

    activas = postulaciones.exclude(
        estado__in=[Postulacion.Estado.DESCARTADA, Postulacion.Estado.CONTRATADA],
    )

    return render(request, 'dashboard/inicio.html', {
        'saludo': _saludo(),
        'empresa': empresa,
        'roles': list(request.user.groups.values_list('name', flat=True)),
        'hoy': timezone.localdate(),
        'vacantes_publicadas': vacantes.filter(estado=Vacante.Estado.PUBLICADA).count(),
        'total_vacantes': vacantes.count(),
        'postulaciones_activas': activas.count(),
        'total_postulaciones': postulaciones.count(),
        'total_personas': personas.count(),
        'empleados_activos': empleados.filter(estado=Empleado.Estado.ACTIVO).count(),
        'total_areas': areas.count(),
        'total_cargos': cargos.count(),
        'pipeline': pipeline,
        'pipeline_mayor': mayor,
        'vacantes_recientes': vacantes.select_related('cargo', 'area').order_by('-fecha_creacion')[:5],
        'postulaciones_recientes': postulaciones.select_related('persona', 'vacante').order_by('-fecha_postulacion')[:5],
    })
