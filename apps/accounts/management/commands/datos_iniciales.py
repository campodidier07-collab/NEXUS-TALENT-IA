from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from apps.accounts.models import Usuario
from apps.organization.models import Area, Cargo, CargoHabilidad, Empresa, Habilidad


ROLES = ('Administrador', 'Reclutador', 'Lider', 'Empleado', 'Candidato')
CORREO_ADMIN = 'admin@nexus.local'
CLAVE_ADMIN = 'NexusAdmin2026'


class Command(BaseCommand):
    help = 'Crea roles, la empresa de prueba y el usuario administrador.'

    def handle(self, *args, **options):
        for nombre in ROLES:
            Group.objects.get_or_create(name=nombre)

        empresa, _ = Empresa.objects.get_or_create(
            nit='900123456-1',
            defaults={
                'nombre': 'NEXUS Demo',
                'correo': 'contacto@nexus.local',
                'telefono': '3000000000',
                'direccion': 'Bogota',
                'activa': True,
            },
        )
        area, _ = Area.objects.get_or_create(
            empresa=empresa,
            nombre='Tecnologia',
            defaults={'activa': True},
        )
        cargo, _ = Cargo.objects.get_or_create(
            empresa=empresa,
            area=area,
            nombre='Analista de talento',
            defaults={
                'descripcion': 'Acompana los procesos de seleccion y seguimiento del talento.',
                'activo': True,
            },
        )

        habilidades = [
            ('Comunicacion', Habilidad.Categoria.BLANDA),
            ('Excel', Habilidad.Categoria.TECNICA),
            ('Python', Habilidad.Categoria.TECNICA),
        ]
        for nombre, categoria in habilidades:
            habilidad, _ = Habilidad.objects.get_or_create(
                empresa=empresa,
                nombre=nombre,
                defaults={'categoria': categoria, 'activa': True},
            )
            CargoHabilidad.objects.get_or_create(
                cargo=cargo,
                habilidad=habilidad,
                defaults={'nivel_requerido': 3, 'obligatoria': nombre != 'Python'},
            )

        if not Usuario.objects.filter(email=CORREO_ADMIN).exists():
            admin = Usuario.objects.create_superuser(
                email=CORREO_ADMIN,
                password=CLAVE_ADMIN,
                nombre='Didier',
                apellido='Admin',
                empresa=empresa,
            )
            admin.groups.add(Group.objects.get(name='Administrador'))
            self.stdout.write(self.style.SUCCESS(
                f'Usuario creado: {CORREO_ADMIN} / {CLAVE_ADMIN}'
            ))
        else:
            self.stdout.write('El usuario administrador ya existia. La clave no se modifico.')

        self.stdout.write(self.style.SUCCESS('Datos iniciales listos.'))
