from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.people.models import Persona
from apps.recruitment.models import Postulacion, Vacante


@login_required
def inicio(request):
    empresa_id = request.user.empresa_id
    vacantes = Vacante.objects.all()
    personas = Persona.objects.all()
    postulaciones = Postulacion.objects.all()
    if empresa_id:
        vacantes = vacantes.filter(empresa_id=empresa_id)
        personas = personas.filter(empresa_id=empresa_id)
        postulaciones = postulaciones.filter(vacante__empresa_id=empresa_id)

    return render(request, 'dashboard/inicio.html', {
        'total_vacantes': vacantes.count(),
        'vacantes_abiertas': vacantes.filter(estado=Vacante.Estado.PUBLICADA).count(),
        'total_personas': personas.count(),
        'total_postulaciones': postulaciones.count(),
    })
