# NEXUS Talent IA

Plataforma de talento humano en Django y MySQL. La inteligencia artificial recomienda y explica; la decisión de contratar o descartar la toma una persona.

Dos personas: Didier (rama `Didier`, lidera la base) y Aileen (rama `Aileen`, todavía no existe). Aileen se crea solo cuando esta base esté fusionada en `main`.

Repositorio: https://github.com/campodidier07-collab/NEXUS-TALENT-IA

## Decisiones cerradas

- Todo el sistema es Django. No hay React ni otra aplicación de frontend.
- La base es MySQL, nombre `nexus_talent`, charset `utf8mb4`. Las tablas las crea `migrate`. No se diseñan a mano.
- El usuario de login es `accounts.Usuario`, con correo. El modelo ya está migrado: no lo reemplaces.
- Hay una sola `persona` para candidato y empleado. Al contratar se agrega `empleado`; no se copia la ficha.
- La compatibilidad es una recomendación. El estado de la postulación lo cambia un usuario y queda en `historial_postulacion`.
- Los roles son grupos de Django: Administrador, Reclutador, Líder, Empleado, Candidato. No crees tablas `rol` ni `permiso`.
- Aileen no modifica `models.py`, `settings.py` ni la plantilla base. Si falta un campo, lo agrega Didier con una migración.

## Ya está hecho

Entorno virtual en `.venv`, Django 5.2.17. Activar con `.\.venv\Scripts\Activate.ps1`.

Apps: `accounts`, `organization`, `people`, `recruitment`, `auditoria`, `dashboard`.

Migraciones aplicadas en MySQL. Datos semilla con `python manage.py datos_iniciales`.

Credenciales locales: `admin@nexus.local` / `NexusAdmin2026`. Empresa de prueba: NEXUS Demo.

Arranque: `python manage.py runserver` y abrir http://127.0.0.1:8000/

Rutas:

- `/` portada pública. Sin sesión el botón es Acceder. Con sesión, Ir al panel.
- `/panel/` resumen interno: vacantes, postulaciones, personas y empleados.
- `/cuentas/ingresar/` login. La recuperación imprime el enlace en la terminal.
- `/admin/` administrador de Django, con las 18 tablas.

La portada y el panel más reciente están en el disco de la rama `Didier` y pueden estar sin commit. La base Django ya se subió a `origin/Didier`. `main` remoto todavía no es la rama de trabajo.

Al cambiar la portada, el panel, el CSS o cualquier pantalla, usa las skills del proyecto en `.agents/skills/`, sobre todo `apple-design` y `emil-design-eng`.

## Qué sigue

1. No recrees el proyecto, el entorno virtual ni los modelos.
2. Revisa la portada y el panel. Si Didier lo pide, haz commit en `Didier` y `git push`.
3. Abre el pull request de `Didier` hacia `main` y fusiónalo. Recién ahí Aileen clona y crea su rama:

```powershell
git clone https://github.com/campodidier07-collab/NEXUS-TALENT-IA.git
cd NEXUS-TALENT-IA
git checkout main
git pull
git checkout -b Aileen
git push -u origin Aileen
```

4. El siguiente módulo de producto es el de Aileen: pantallas de vacantes, registro de persona, carga de hoja de vida y lista de postulaciones, usando los modelos que ya existen.
5. El análisis con IA (extracción de hoja de vida, compatibilidad explicable y preguntas de entrevista) va después de que esas pantallas guarden datos reales. No lo implementes antes.
6. Capacitaciones, evaluaciones de desempeño, rutas y notificaciones quedan fuera de esta versión.

Cada uno trabaja en su rama. `main` solo recibe pull requests. Antes de seguir, traer `main` a la rama propia:

```powershell
git checkout main
git pull
git checkout Didier
git merge main
git push
```

Aileen usa el mismo bloque con el nombre `Aileen`.
