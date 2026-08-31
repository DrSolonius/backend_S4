# Sistema Académico — API de estudiantes

Proyecto educativo para aprender a construir una API HTTP con FastAPI, organizar el código por capas y utilizar DTO con Pydantic.

La aplicación permite crear, consultar, actualizar, eliminar y listar estudiantes con paginación. Los datos se guardan **en memoria**, dentro de un diccionario de Python. No utiliza una base de datos, SQLAlchemy, una carpeta `shared` ni una carpeta `modules`.

## Requisitos

- Python 3.14 o superior, según el `pyproject.toml` del proyecto.
- uv instalado.
- Git, si vas a clonar el repositorio.

## Instalación y ejecución

Si todavía no tienes el proyecto en tu computador:

```powershell
git clone https://github.com/DrSolonius/backend_S4.git
cd backend_S4
```

Si ya lo tienes, abre una terminal en la raíz del proyecto: la carpeta que contiene `pyproject.toml`, `app`, `application`, `domain`, `infrastructure` y `presentation`.

Instala las dependencias y ejecuta el servidor:

```powershell
uv sync
uv run uvicorn app.main:app --reload
```

No necesitas activar manualmente el entorno virtual para usar `uv run`.

- Documentación interactiva: [Swagger UI](http://127.0.0.1:8000/docs).
- Documentación alternativa: [ReDoc](http://127.0.0.1:8000/redoc).
- Listado de estudiantes: [GET /estudiantes](http://127.0.0.1:8000/estudiantes).

Para detener el servidor, presiona **Ctrl + C**. La opción `--reload` reinicia el servidor cuando guardas cambios en el código.

> La ruta `/` no está implementada. Un error 404 al abrir `http://127.0.0.1:8000/` no significa que el servidor haya fallado; abre `/docs`.

## Estructura por capas

```text
backend_S4/
├── app/
│   └── main.py
├── application/
│   └── services/
│       └── estudiante_service.py
├── domain/
│   └── estudiante.py
├── infrastructure/
│   └── repositories/
│       └── estudiante_repository.py
├── presentation/
│   ├── dtos/
│   │   ├── estudiante_dto.py
│   │   └── estudiante_query_dto.py
│   └── routers/
│       └── estudiante_router.py
├── pyproject.toml
└── uv.lock
```

| Parte | Responsabilidad |
|---|---|
| `app/main.py` | Crea la aplicación FastAPI y registra el router. |
| Presentación | Recibe solicitudes HTTP, valida los datos con DTO y prepara las respuestas. |
| Aplicación | Coordina las operaciones, comprueba correos duplicados y calcula la paginación. |
| Dominio | Define la entidad `Estudiante`, sus validaciones básicas y sus comportamientos. |
| Infraestructura | Guarda y recupera estudiantes mediante un repositorio en memoria. |

Este ejemplo utiliza un servicio que depende de un repositorio concreto para mantener sencilla la primera implementación. No pretende implementar todos los patrones de arquitectura limpia.

## ¿Qué es un DTO?

DTO significa **Data Transfer Object**, u objeto de transferencia de datos. Define la estructura de los datos que entran o salen de la API.

En este proyecto, los DTO son clases de Pydantic ubicadas en `presentation/dtos`. FastAPI los utiliza al procesar solicitudes y respuestas; no se ejecutan como procesos separados.

| DTO | Uso |
|---|---|
| `EstudianteCreateDTO` | Valida `nombre`, `apellido` y `email` al crear un estudiante. |
| `EstudianteUpdateDTO` | Valida esos tres campos al actualizar. Todos son obligatorios. |
| `EstudianteQueryDTO` | Valida `pagina` y `tamano`, recibidos como parámetros de la URL. |
| `EstudianteResponseDTO` | Define los datos que devuelve la API de un estudiante. |
| `EstudiantePaginaDTO` | Contiene `items`, `total`, `pagina` y `tamano`. |

El frontend se comunica con la API mediante HTTP. Envía y recibe JSON; no recibe objetos Python. Los DTO definen la estructura de esos datos, pero no son la conexión de red.

### Configuración de Pydantic

En los DTO de creación y actualización:

```python
model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid",
)
```

- `str_strip_whitespace=True`: elimina espacios al principio y al final. Por ejemplo, `"  Ana  "` se convierte en `"Ana"`.
- `extra="forbid"`: rechaza campos no definidos en el DTO, como `administrador`.
- `Field(min_length=1)`: impide textos vacíos. Un nombre compuesto solo de espacios también se rechaza después de limpiarlo.

Los nombres y apellidos admiten entre 1 y 100 caracteres. El correo admite entre 1 y 254 caracteres.

> En la versión actual, `email` es de tipo `str`: se valida su longitud, pero **no su formato de correo electrónico**. Un texto como `"hola"` puede ser aceptado. Validar el formato con `EmailStr` sería una mejora posterior.

### DTO, dominio y mapeo

`domain/estudiante.py` define una entidad con `dataclass`. No utiliza Pydantic. Al crear la entidad, `__post_init__()` limpia espacios y comprueba que nombre, apellido y correo no estén vacíos.

La entidad también ofrece la propiedad `nombre_completo` y los métodos `activar()` y `desactivar()`. Estos dos métodos todavía no tienen endpoints en el router actual.

El DTO de respuesta utiliza:

```python
model_config = ConfigDict(from_attributes=True)
```

Esto permite leer atributos de un objeto del dominio. El router realiza el mapeo así:

```python
respuesta = EstudianteResponseDTO.model_validate(estudiante)
```

Pydantic obtiene los atributos correspondientes, valida sus valores y construye el DTO. También puede leer la propiedad `nombre_completo`.

No hay un archivo mapper separado porque esta conversión es directa. Un mapper explícito sería útil si hubiera que combinar, renombrar o transformar campos con reglas adicionales.

El repositorio debe asignar el ID antes de construir el DTO de respuesta, porque este exige `id: int` y no acepta `None`.

## Recorrido de una solicitud

Para crear un estudiante:

```text
Cliente envía POST /estudiantes con JSON
    ↓
FastAPI valida el cuerpo con EstudianteCreateDTO
    ↓
Router pasa los datos al servicio
    ↓
Servicio crea la entidad Estudiante y verifica el correo duplicado
    ↓
Repositorio asigna un ID y guarda una copia en memoria
    ↓
Servicio devuelve la entidad al router
    ↓
Pydantic la convierte a EstudianteResponseDTO
    ↓
FastAPI responde con JSON y estado 201
```

El dominio no es una parada adicional: define el objeto `Estudiante` que utilizan servicio y repositorio. El servicio usa sus reglas cuando crea la entidad o llama a sus métodos.

Si el DTO rechaza los datos de entrada, FastAPI responde con **422** antes de ejecutar la función del router y el servicio.

## Endpoints disponibles

| Método | Ruta | Acción | Respuesta exitosa |
|---|---|---|---|
| POST | `/estudiantes` | Crear un estudiante. | 201 y estudiante creado. |
| GET | `/estudiantes` | Listar con paginación. | 200 y página de resultados. |
| GET | `/estudiantes/{estudiante_id}` | Consultar por ID. | 200 y estudiante. |
| PUT | `/estudiantes/{estudiante_id}` | Actualizar nombre, apellido y correo. | 200 y estudiante actualizado. |
| DELETE | `/estudiantes/{estudiante_id}` | Eliminar el registro de memoria. | 204, sin cuerpo. |

`PUT` requiere los tres campos editables; no es una actualización parcial. Conserva el estado `activo` que ya tenía el estudiante. `DELETE` elimina el registro; no llama al método `desactivar()`.

## Prueba paso a paso en Swagger

Abre [Swagger UI](http://127.0.0.1:8000/docs), despliega un endpoint, pulsa **Try it out**, completa sus datos y pulsa **Execute**.

### 1. Crear un estudiante

Usa `POST /estudiantes`:

```json
{
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com"
}
```

En una ejecución nueva, el primer estudiante tendrá ID 1. Respuesta esperada, con código **201**:

```json
{
  "id": 1,
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com",
  "activo": true,
  "nombre_completo": "Ana Pérez"
}
```

### 2. Consultar y listar

Consulta el ID devuelto usando `GET /estudiantes/{estudiante_id}`.

Luego usa `GET /estudiantes` con `pagina=1` y `tamano=5`. Si solo creaste el estudiante del ejemplo, recibirás:

```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Ana",
      "apellido": "Pérez",
      "email": "ana@example.com",
      "activo": true,
      "nombre_completo": "Ana Pérez"
    }
  ],
  "total": 1,
  "pagina": 1,
  "tamano": 5
}
```

`tamano` es el máximo solicitado, no necesariamente la cantidad de elementos recibidos. `total` cuenta todos los estudiantes guardados, no solo los de esa página.

### 3. Actualizar

Usa `PUT /estudiantes/1` con:

```json
{
  "nombre": "Ana María",
  "apellido": "Pérez",
  "email": "ana@example.com"
}
```

Se permite conservar el propio correo. Si el correo pertenece a otro estudiante, la operación se rechaza.

### 4. Comprobar validaciones

| Prueba | Resultado esperado |
|---|---|
| Crear con `nombre` vacío o solo espacios. | 422. |
| Crear agregando un campo `administrador`. | 422. |
| Crear o actualizar con un correo de otro estudiante. | 400. |
| Listar con `pagina=0` o `tamano=101`. | 422. |
| Consultar, actualizar o eliminar un ID positivo inexistente. | 404. |
| Usar ID 0 o negativo en una ruta de estudiante. | 422. |

La comparación de correos duplicados ignora mayúsculas y espacios exteriores. Por ejemplo, `ANA@example.com` y `ana@example.com` se consideran el mismo correo.

### 5. Eliminar

Usa `DELETE /estudiantes/1`. Debe responder **204** sin contenido. Si vuelves a consultar ese ID, debe responder **404**.

## Cómo funciona la paginación

Ejemplo de solicitud:

```http
GET /estudiantes?pagina=2&tamano=5
```

1. `EstudianteQueryDTO` valida los parámetros. Por defecto usa página 1 y tamaño 10; el tamaño permitido es de 1 a 100.
2. El servicio calcula `offset = (pagina - 1) * tamano`.
3. El repositorio ordena por ID y selecciona la parte correspondiente de la lista.
4. El router construye `EstudiantePaginaDTO` con los resultados y el total.

Con página 2 y tamaño 5, `offset` vale 5: se saltan los primeros cinco registros y se devuelven hasta cinco más. Una página fuera de los resultados devuelve `items: []` con código 200, conservando el total real.

## Consideraciones del almacenamiento en memoria

- La instancia `estudiante_repository` se reutiliza entre solicitudes del mismo proceso.
- Los datos se pierden cuando el servidor se detiene o reinicia, incluso por `--reload`.
- No ejecutes este ejemplo con varios workers: cada proceso tendría su propio diccionario.
- El repositorio usa copias para evitar que modificar un objeto devuelto cambie accidentalmente el registro almacenado.
- La versión didáctica no incorpora bloqueos ni transacciones para solicitudes simultáneas. No garantiza IDs y correos únicos bajo concurrencia.
- No incluye autenticación ni permisos. No debe exponerse públicamente con datos reales de estudiantes.

## Problemas frecuentes

### `No module named 'app'`

Ejecuta el servidor desde la raíz, no desde dentro de `app`. En PowerShell puedes comprobarlo con:

```powershell
Get-Location
Get-ChildItem
Test-Path .\app\main.py
```

El último comando debe devolver `True`.

### `cannot import name 'EstudianteRepository'`

Comprueba que el archivo `infrastructure/repositories/estudiante_repository.py` esté guardado y contenga tanto la clase `EstudianteRepository` como la instancia:

```python
estudiante_repository = EstudianteRepository()
```

### No aparecen endpoints en Swagger

Comprueba que `app/main.py` tenga:

```python
from fastapi import FastAPI
from presentation.routers.estudiante_router import router

app = FastAPI(title="Sistema Académico")
app.include_router(router)
```

## Archivos que no deben subirse a Git

Crea un `.gitignore` en la raíz con:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.env
```

Sí debes conservar `pyproject.toml` y `uv.lock`. Si los archivos `__pycache__` ya están publicados, agregar estas reglas no los retira del seguimiento: hace falta quitarlos también del índice de Git.
