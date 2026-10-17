# Sistema Académico — API de estudiantes

Proyecto educativo para aprender a construir una API HTTP con **FastAPI**, organizar el código por capas y utilizar **Pydantic, DTO, schemas, servicios, dominio y repositorios**.

La aplicación permite crear, consultar, actualizar, eliminar y listar estudiantes y cursos con paginación, e inscribir estudiantes en cursos (un estudiante puede tomar n cursos y un curso puede tener n estudiantes).

En esta etapa:

- Los datos se almacenan en **PostgreSQL** mediante el ORM **SQLAlchemy 2.1** (driver `psycopg2`).
- La relación estudiante ↔ curso es **muchos a muchos** con la tabla de asociación `inscripciones`.
- Los **mappers** convierten entre entidades de dominio y modelos ORM.
- Cada solicitud recibe su propia sesión de base de datos mediante `Depends`.
- Los DTO están organizados dentro de `presentation/schemas/dtos/`.
- Se utilizan **seeders** que cargan 60 estudiantes, 10 cursos y 180 inscripciones si la base de datos está vacía.

---

## Requisitos

- Python 3.14 o superior.
- `uv` instalado.
- Git.
- PostgreSQL corriendo localmente.

---

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/DrSolonius/backend_S4.git
cd backend_S4
```

Instala las dependencias:

```bash
uv sync
```

Configura la conexión a PostgreSQL copiando `.env.example` como `.env` y completando tus datos:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clase
DB_USER=alumno
DB_PASSWORD=mi_clave_segura
```

La base de datos indicada en `DB_NAME` debe existir.

Crea las tablas aplicando las migraciones con Alembic:

```bash
uv run alembic upgrade head
```

---

## Ejecutar la API

Desde la raíz del proyecto:

```bash
uv run uvicorn app.main:app --reload
```

Por defecto Uvicorn utiliza el puerto `8000`.

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Si el puerto está ocupado, puedes utilizar otro:

```bash
uv run uvicorn app.main:app --reload --port 8765
```

---

## Estructura del proyecto

```text
backend_S4/
├── .vscode/
│   ├── launch.json
│   └── settings.json
│
├── app/
│   └── main.py
│
├── application/
│   └── services/
│       └── estudiante_service.py
│
├── domain/
│   └── estudiante.py
│
├── infrastructure/
│   ├── repositories/
│   │   └── estudiante_repository.py
│   │
│   └── seeders/
│       └── estudiante_seeder.py
│
├── presentation/
│   ├── routers/
│   │   └── estudiante_router.py
│   │
│   └── schemas/
│       └── dtos/
│           ├── estudiante_dto.py
│           └── estudiante_query_dto.py
│
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## Responsabilidad de cada capa

| Componente | Responsabilidad |
|---|---|
| `app/main.py` | Crea la aplicación FastAPI, carga los datos iniciales y registra los routers. |
| `presentation/routers` | Define los endpoints y recibe las solicitudes HTTP. |
| `presentation/schemas` | Agrupa las estructuras relacionadas con entrada, salida y validación de la API. |
| `presentation/schemas/dtos` | Contiene los DTO implementados con Pydantic. |
| `application/services` | Coordina los casos de uso y las reglas de aplicación. |
| `domain` | Define la entidad `Estudiante`, su estado y comportamiento. |
| `infrastructure/repositories` | Guarda y recupera estudiantes desde memoria. |
| `infrastructure/seeders` | Carga datos iniciales para pruebas. |

---

## Arquitectura actual

```text
CLIENTE
   │
   │ HTTP / JSON
   ▼
┌─────────────────────────────────┐
│ PRESENTATION                    │
│                                 │
│ Router                          │
│ + DTO / Pydantic                │
│ + Validaciones                  │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ APPLICATION                     │
│                                 │
│ EstudianteService               │
│ Casos de uso y coordinación     │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ DOMAIN                          │
│                                 │
│ Estudiante                      │
│ Estado y comportamiento         │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ INFRASTRUCTURE                  │
│                                 │
│ EstudianteRepository            │
│ Almacenamiento en memoria       │
└─────────────────────────────────┘
```

Flujo simplificado:

```text
Cliente
   ↓
HTTP / JSON
   ↓
Router + DTO Pydantic
   ↓
Service
   ↓
Entidad de dominio
   ↓
Repository
   ↓
Memoria
```

---

## ¿Qué es un schema?

En este proyecto, `schemas/` agrupa las estructuras utilizadas por la capa de presentación para definir cómo deben verse los datos que entran y salen de la API.

Actualmente los DTO son clases de Pydantic, por lo que ya cumplen funciones de:

- definición de estructura;
- validación;
- transformación;
- serialización.

Por eso se organizan así:

```text
presentation/
└── schemas/
    └── dtos/
        ├── estudiante_dto.py
        └── estudiante_query_dto.py
```

No se crea un archivo `estudiante_schema.py` adicional porque duplicaría responsabilidades en esta etapa.

---

## ¿Qué es un DTO?

DTO significa **Data Transfer Object**.

Un DTO representa datos que se transfieren entre componentes.

| DTO | Responsabilidad |
|---|---|
| `EstudianteCreateDTO` | Define y valida los datos necesarios para crear un estudiante. |
| `EstudianteUpdateDTO` | Define y valida los datos necesarios para actualizar un estudiante. |
| `EstudianteResponseDTO` | Define la estructura de un estudiante devuelto por la API. |
| `EstudiantePaginaDTO` | Define la respuesta paginada. |
| `EstudianteQueryDTO` | Valida los parámetros `pagina` y `tamano`. |

Los DTO se encuentran en:

```text
presentation/schemas/dtos/
```

---

## DTO y entidad de dominio

```text
EstudianteCreateDTO
        │
        │ datos de entrada
        ▼
EstudianteService
        │
        │ crea
        ▼
Estudiante
```

`EstudianteCreateDTO` pertenece a la frontera de la API.

`Estudiante` representa el objeto del dominio.

---

## Validación con Pydantic

Ejemplo:

```python
class EstudianteCreateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=254)
```

Esto permite validar automáticamente los datos recibidos.

Ejemplo válido:

```json
{
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com"
}
```

---

## Parámetros de paginación

```python
class EstudianteQueryDTO(BaseModel):
    pagina: int = Field(default=1, ge=1)
    tamano: int = Field(default=10, ge=1, le=100)
```

Esto significa:

```text
pagina >= 1
1 <= tamano <= 100
```

Valores por defecto:

```text
pagina = 1
tamano = 10
```

Ejemplo:

```http
GET /estudiantes?pagina=2&tamano=10
```

---

## Cómo funciona la paginación

El servicio calcula:

```python
offset = (pagina - 1) * tamano
```

Ejemplo:

```text
pagina = 3
tamano = 10

offset = (3 - 1) * 10
offset = 20
```

Con 60 estudiantes:

```text
Página 1 → registros 1 al 10
Página 2 → registros 11 al 20
Página 3 → registros 21 al 30
Página 4 → registros 31 al 40
Página 5 → registros 41 al 50
Página 6 → registros 51 al 60
Página 7 → sin resultados
```

---

## Seeder

El proyecto incluye:

```text
infrastructure/
└── seeders/
    └── estudiante_seeder.py
```

El seeder carga **60 estudiantes de prueba** en memoria cuando se inicia la aplicación.

Flujo:

```text
main.py
   ↓
seed_estudiantes()
   ↓
EstudianteService
   ↓
EstudianteRepository
   ↓
Memoria
```

`app/main.py` ejecuta:

```python
service = EstudianteService(estudiante_repository)

seed_estudiantes(service)
```

---

## Persistencia con SQLAlchemy

```text
Service
   ↓  entidad de dominio (Estudiante, Curso)
Repository
   ↓  mapper
Modelo ORM (EstudianteModel, CursoModel)
   ↓  Session
PostgreSQL
```

Archivos nuevos en `infrastructure/`:

| Archivo | Responsabilidad |
|---|---|
| `database.py` | Lee el `.env`, crea el `engine` de PostgreSQL, la `SessionLocal`, la clase `Base` y las tablas. |
| `models/estudiante_model.py` | Tabla `estudiantes`. |
| `models/curso_model.py` | Tabla `cursos`. |
| `models/inscripcion_model.py` | Tabla de asociación `inscripciones` (muchos a muchos). |
| `mappers/*_mapper.py` | Convierten entre entidad de dominio y modelo ORM. |

Además, `presentation/dependencies.py` abre una sesión por solicitud y construye los servicios con `Depends`.

Esto significa que:

- los datos se conservan al detener el servidor;
- las tablas se crean y modifican con migraciones de Alembic (ver más abajo);
- los seeders solo se ejecutan cuando la base de datos está vacía;
- para empezar de cero: `uv run alembic downgrade base` y luego `uv run alembic upgrade head`;
- la conexión se configura con las variables `DB_*` del archivo `.env`;
- las migraciones viven en `migrations/versions/`.

---

## Migraciones con Alembic

Alembic guarda en la tabla `alembic_version` qué migración está aplicada en la base de datos. `migrations/env.py` usa el mismo `engine` que la aplicación, así que también lee la conexión desde el `.env`.

```text
backend_S4/
├── alembic.ini
└── migrations/
    ├── env.py
    ├── script.py.mako
    └── versions/
        └── 0001_crear_tablas.py
```

| Comando | Qué hace |
|---|---|
| `uv run alembic upgrade head` | Aplica todas las migraciones pendientes. |
| `uv run alembic downgrade -1` | Deshace la última migración. |
| `uv run alembic current` | Muestra la migración aplicada. |
| `uv run alembic history` | Lista todas las migraciones. |
| `uv run alembic revision --autogenerate -m "mensaje"` | Crea una migración comparando los modelos con la base de datos. |
| `uv run alembic check` | Indica si hay cambios en los modelos sin migración. |

Flujo para cambiar un modelo (por ejemplo, agregar una columna):

```text
1. Modificar el modelo en infrastructure/models/
2. uv run alembic revision --autogenerate -m "agregar columna telefono"
3. Revisar el archivo generado en migrations/versions/
4. uv run alembic upgrade head
```

Si las tablas ya existían antes de usar Alembic (creadas con `create_all`), no ejecutes `upgrade` sobre ellas: marca la base de datos como actualizada con

```bash
uv run alembic stamp head
```

---

## ¿Por qué no existe Mapper todavía?

Un mapper transforma una representación en otra.

Ejemplo futuro:

```text
DTO
 ↓
Entidad de dominio
 ↓
Modelo ORM
 ↓
Base de datos
```

Actualmente tenemos:

```text
DTO
 ↓
Entidad de dominio
 ↓
Repositorio en memoria
```

Para construir el DTO de respuesta se utiliza directamente:

```python
EstudianteResponseDTO.model_validate(estudiante)
```

Resumen:

```text
Schema  → define estructura y validación
DTO     → transporta datos
Mapper  → transforma una representación en otra
```

---

## Recorrido de una solicitud POST

Solicitud:

```http
POST /estudiantes
```

Body:

```json
{
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com"
}
```

Recorrido:

```text
Cliente
   │
   │ POST /estudiantes
   │ JSON
   ▼
FastAPI
   │
   ▼
EstudianteCreateDTO
   │
   │ valida
   ▼
Router
   │
   ▼
EstudianteService
   │
   │ crea Estudiante
   │ verifica email
   ▼
EstudianteRepository
   │
   │ asigna ID
   │ guarda en memoria
   ▼
EstudianteService
   │
   ▼
Router
   │
   ▼
EstudianteResponseDTO
   │
   ▼
FastAPI
   │
   │ JSON + HTTP 201
   ▼
Cliente
```

---

## Endpoints disponibles

| Método | Endpoint | Acción |
|---|---|---|
| `POST` | `/estudiantes` | Crear estudiante |
| `GET` | `/estudiantes` | Listar estudiantes con paginación |
| `GET` | `/estudiantes/{estudiante_id}` | Obtener estudiante |
| `PUT` | `/estudiantes/{estudiante_id}` | Actualizar estudiante |
| `DELETE` | `/estudiantes/{estudiante_id}` | Eliminar estudiante |

---

## Probar la API con Swagger

Ejecuta:

```bash
uv run uvicorn app.main:app --reload
```

Luego abre:

```text
http://127.0.0.1:8000/docs
```

Prueba:

```http
GET /estudiantes?pagina=1&tamano=10
```

Respuesta paginada:

```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Ana",
      "apellido": "Pérez",
      "email": "estudiante01@example.com",
      "activo": true,
      "nombre_completo": "Ana Pérez"
    }
  ],
  "total": 60,
  "pagina": 1,
  "tamano": 10
}
```

La lista real contendrá hasta 10 estudiantes.

Para probar la paginación:

```text
pagina=1  tamano=10
pagina=2  tamano=10
pagina=3  tamano=10
pagina=6  tamano=10
pagina=7  tamano=10
```

La página 7 debe devolver una lista vacía:

```json
{
  "items": [],
  "total": 60,
  "pagina": 7,
  "tamano": 10
}
```

---

## Códigos HTTP importantes

| Código | Significado |
|---|---|
| `200 OK` | Solicitud procesada correctamente |
| `201 Created` | Estudiante creado |
| `204 No Content` | Estudiante eliminado |
| `400 Bad Request` | Regla de aplicación inválida |
| `404 Not Found` | Estudiante inexistente |
| `422 Unprocessable Entity` | Error de validación |

---

## Depuración con VS Code

El proyecto incluye:

```text
.vscode/
├── launch.json
└── settings.json
```

Para iniciar la depuración:

```text
Ctrl + Shift + D
```

Selecciona:

```text
Depurar API de estudiantes
```

y presiona:

```text
F5
```

La configuración actual de `launch.json` utiliza el puerto:

```text
8001
```

Si ese puerto está ocupado, cambia el valor en `.vscode/launch.json`.

| Tecla | Acción |
|---|---|
| `F9` | Agregar o quitar breakpoint |
| `F10` | Avanzar sin entrar en una función |
| `F11` | Entrar en una función |
| `Shift + F11` | Salir de una función |
| `F5` | Continuar ejecución |
| `Shift + F5` | Detener depuración |

Referencia: [Depuración de Python en VS Code](https://code.visualstudio.com/docs/python/debugging).

---

## Problemas frecuentes

### Address already in use

Si aparece:

```text
ERROR: [Errno 98] Address already in use
```

el puerto ya está siendo utilizado.

En Linux o WSL:

```bash
sudo ss -ltnp | grep :8000
```

Puedes iniciar Uvicorn en otro puerto:

```bash
uv run uvicorn app.main:app --reload --port 8765
```

### No module named 'presentation.dtos'

La ruta antigua:

```python
from presentation.dtos.estudiante_dto import ...
```

ya no corresponde a la estructura actual.

La ruta correcta es:

```python
from presentation.schemas.dtos.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudiantePaginaDTO,
)
```

y:

```python
from presentation.schemas.dtos.estudiante_query_dto import (
    EstudianteQueryDTO,
)
```

### No module named 'app'

Ejecuta Uvicorn desde:

```text
backend_S4/
```

El comando correcto es:

```bash
uv run uvicorn app.main:app --reload
```

---

## Estado actual del proyecto

Actualmente se trabajan:

- FastAPI.
- Uvicorn.
- HTTP.
- JSON.
- CRUD.
- Rutas.
- Parámetros de ruta.
- Parámetros de consulta.
- Pydantic.
- Schemas.
- DTO.
- Validaciones.
- Entidad de dominio.
- Servicios.
- Repositorios.
- Almacenamiento en memoria.
- Seeder.
- Paginación.
- Códigos de estado HTTP.
- Swagger / OpenAPI.
- Separación de responsabilidades.

Todavía no se incorporan:

- Autenticación.
- Autorización.
- Docker.
- CI/CD.

El proyecto continuará evolucionando progresivamente durante el curso.
