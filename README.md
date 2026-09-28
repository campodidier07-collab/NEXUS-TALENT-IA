# NEXUS Talent IA

Sistema inteligente para gestionar y potenciar el talento humano.

Plataforma web en Django y MySQL. La inteligencia artificial recomienda y explica; las decisiones de seleccion quedan en manos del equipo de talento humano.

## Ramas

- `main` recibe solo lo que ya esta listo, mediante un pull request.
- `Didier` es la rama de la base del proyecto: modelo de datos, acceso y vista principal.
- `Ailyn` es la rama de vacantes, candidatos y postulaciones. Se crea cuando la base ya esta en `main`.

## Arranque local

Requiere Python 3.10 y MySQL en ejecucion.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Crea la base vacia y copia el archivo de entorno:

```sql
CREATE DATABASE nexus_talent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```powershell
copy .env.example .env
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py datos_iniciales
.\.venv\Scripts\python manage.py runserver
```

El ingreso de prueba queda en `admin@nexus.local` / `NexusAdmin2026`.
El enlace de recuperacion de contrasena se imprime en la terminal.

## Apps

| App | Responsable ahora | Contenido |
|---|---|---|
| `accounts` | Didier | Usuario, login y recuperacion de contrasena |
| `organization` | Didier | Empresa, area, cargo y habilidades |
| `people` | Didier | Persona, hoja de vida y empleado |
| `recruitment` | Aileen, pantallas | Vacante, postulacion, entrevista y analisis |
| `auditoria` | Didier | Registro de acciones |
| `dashboard` | Didier | Vista de inicio |
