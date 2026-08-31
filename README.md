Sistema Académico — API de estudiantes

Proyecto educativo para aprender a construir una API HTTP con FastAPI, organizar el código por capas y utilizar schemas y DTO con Pydantic.

La aplicación permite crear, consultar, actualizar, eliminar y listar estudiantes con paginación. Los datos se guardan en memoria, dentro de un diccionario de Python. No utiliza una base de datos ni SQLAlchemy.

En esta etapa del proyecto:

schemas/ agrupa los contratos y validaciones utilizados por la capa de presentación.

dtos/ se mantiene dentro de schemas/ para representar los objetos de transferencia de datos usados por la API.

No se utiliza un mapper separado porque las conversiones actuales son directas.

El repositorio utiliza almacenamiento en memoria.

Requisitos

Python 3.14 o superior, según el pyproject.toml del proyecto.

uv instalado.

Git, si vas a clonar el repositorio.

Instalación y ejecución

Si todavía no tienes el proyecto en tu computador:

git clone https://github.com/DrSolonius/backend_S4.git
cd backend_S4

Si ya lo tienes, abre una terminal en la raíz del proyecto: la carpeta que contiene pyproject.toml, app, application, domain, infrastructure y presentation.

Instala las dependencias y ejecuta el servidor:

uv sync
uv run uvicorn app.main:app --reload

No necesitas activar manualmente el entorno virtual para usar uv run.

Documentación interactiva: Swagger UI.

Documentación alternativa: ReDoc.

Listado de estudiantes: GET /estudiantes.

Para detener el servidor, presiona Ctrl + C. La opción --reload reinicia el servidor cuando guardas cambios en el código.

La ruta / no está implementada. Un error 404 al abrir http://127.0.0.1:8000/ no significa que el servidor haya fallado; abre /docs.

Depuración con VS Code (Windows)

La depuración permite detener una solicitud en una línea del código, inspeccionar variables y seguir el recorrido entre router, DTO, servicio, dominio y repositorio.

1. Preparar el entorno

Abre en VS Code la raíz del proyecto: la carpeta que contiene pyproject.toml, .vscode y app.

Instala las extensiones Python y Python Debugger, ambas de Microsoft.

Ejecuta en la terminal integrada:

uv sync

Presiona Ctrl + Shift + P, busca Python: Select Interpreter y selecciona .venv\Scripts\python.exe. Si no aparece, utiliza la opción para introducir la ruta del intérprete.

2. Usar la configuración incluida

El repositorio ya incluye .vscode/launch.json, con la configuración Depurar API de estudiantes. No necesitas crear otra.

Configuración

Función

type: debugpy

Utiliza el depurador de Python.

module: uvicorn

Inicia el servidor Uvicorn dentro del depurador.

python

Usa el ejecutable de .venv/Scripts/python.exe.

app.main:app

Carga la variable app definida en app/main.py.

cwd: ${workspaceFolder}

Ejecuta desde la carpeta abierta en VS Code.

justMyCode: true

Permite concentrarse en el código del proyecto al avanzar paso a paso.

La ruta del intérprete está configurada para Windows. En Linux o macOS debe adaptarse a ${workspaceFolder}/.venv/bin/python.

3. Colocar un punto de interrupción

Abre application/services/estudiante_service.py. Dentro del método crear(), haz clic a la izquierda del número de línea de:

estudiante = Estudiante(

Aparecerá un punto rojo. El depurador pausará la ejecución antes de ejecutar esa línea.

4. Iniciar y enviar una solicitud

Si ya ejecutaste Uvicorn desde una terminal, detenlo con Ctrl + C para liberar el puerto 8000.

Abre Run and Debug / Ejecutar y depurar con Ctrl + Shift + D.

Selecciona Depurar API de estudiantes y presiona F5.

Espera a que el servidor termine de iniciar y abre Swagger UI.

En POST /estudiantes, pulsa Try it out, envía el siguiente cuerpo y pulsa Execute:

{
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com"
}

VS Code se detendrá en el punto rojo. En Variables o al pasar el cursor sobre una variable, podrás revisar nombre, apellido y email. Cuando la construcción de la entidad termine, podrás inspeccionar también estudiante.

Mientras la solicitud esté pausada, Swagger seguirá esperando la respuesta. Presiona F5 para continuar. Si el cuerpo no pasa la validación del DTO, FastAPI devuelve 422 antes de llegar al servicio y ese punto de interrupción no se activa.

5. Avanzar por el código

Tecla

Acción

F9

Agregar o quitar un punto de interrupción en la línea actual.

F10

Ejecutar la línea actual sin entrar en sus funciones.

F11

Entrar en una función cuando sea posible.

Shift + F11

Continuar hasta salir de la función actual.

F5

Continuar hasta el siguiente punto de interrupción.

Shift + F5

Detener la depuración.

Para observar distintas capas, coloca puntos también en crear_estudiante() del router, __post_init__() del dominio y crear() del repositorio. El panel Call Stack / Pila de llamadas muestra qué funciones llevaron a la línea actual.

6. Reiniciar y resolver problemas

La configuración no utiliza --reload. Después de cambiar el código, detén y vuelve a iniciar la depuración.

Cada reinicio borra los estudiantes guardados en memoria.

Si el puerto 8000 está ocupado, detén el otro servidor antes de presionar F5.

Si no se encuentra el intérprete, comprueba que ejecutaste uv sync en la raíz y que existe .venv\Scripts\python.exe.

Si aparece Could not import module "main", verifica que se está usando la configuración incluida, cuyo argumento es app.main:app.

Si aparece No module named 'app', revisa que la carpeta abierta en VS Code contenga directamente app/main.py.

Si no se activa el punto rojo, confirma que lo colocaste en una línea ejecutable del endpoint solicitado y que enviaste la solicitud al servidor iniciado con F5.

Referencia: Depuración de Python en VS Code.

Estructura por capas

backend_S4/
├── .vscode/
│   └── launch.json
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
│   └── repositories/
│       └── estudiante_repository.py
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
├── pyproject.toml
└── uv.lock

Responsabilidad de cada parte

Parte

Responsabilidad

app/main.py

Crea la aplicación FastAPI y registra el router.

presentation/routers

Define los endpoints HTTP y coordina la entrada y salida de la API.

presentation/schemas

Agrupa los contratos y validaciones asociados a la capa de presentación.

presentation/schemas/dtos

Contiene los DTO Pydantic utilizados para transportar y validar datos de entrada y salida.

application/services

Coordina las operaciones, comprueba correos duplicados y calcula la paginación.

domain

Define la entidad Estudiante, sus validaciones básicas y sus comportamientos.

infrastructure/repositories

Guarda y recupera estudiantes mediante un repositorio en memoria.

Este ejemplo utiliza un servicio que depende de un repositorio concreto para mantener sencilla la primera implementación. No pretende implementar todos los patrones de arquitectura limpia.

¿Qué es un schema?

En este proyecto, schemas/ es una carpeta de organización de la capa de presentación.

Su propósito es agrupar las estructuras que definen cómo deben verse y validarse los datos utilizados por la API.

Conceptualmente:

JSON
 ↓
Schema / DTO Pydantic
 ↓
Router
 ↓
Service
 ↓
Dominio
 ↓
Repositorio en memoria

En esta versión no existe un archivo estudiante_schema.py separado porque los DTO actuales ya utilizan Pydantic y cumplen la función de definir estructura y validación.

Por eso la estructura utilizada es:

schemas/
└── dtos/

Esto permite conservar explícitamente el concepto de DTO sin duplicar clases innecesariamente.

¿Qué es un DTO?

DTO significa Data Transfer Object, u objeto de transferencia de datos.

Un DTO representa los datos que se transfieren entre componentes. En este proyecto, además, los DTO son clases de Pydantic, por lo que también permiten validar los datos que recibe o devuelve la API.

Los DTO están ubicados en:

presentation/schemas/dtos/

DTO

Uso

EstudianteCreateDTO

Valida nombre, apellido y email al crear un estudiante.

EstudianteUpdateDTO

Valida esos tres campos al actualizar. Todos son obligatorios.

EstudianteQueryDTO

Valida pagina y tamano, recibidos como parámetros de la URL.

EstudianteResponseDTO

Define los datos que devuelve la API de un estudiante.

EstudiantePaginaDTO

Contiene items, total, pagina y tamano.

El frontend se comunica con la API mediante HTTP. Envía y recibe JSON; no recibe objetos Python.

Los DTO definen la estructura de esos datos, pero no constituyen la conexión de red.

Configuración de Pydantic

En los DTO de creación y actualización:

model_config = ConfigDict(
    str_strip_whitespace=True,
    extra="forbid",
)

str_strip_whitespace=True: elimina espacios al principio y al final. Por ejemplo, "  Ana  " se convierte en "Ana".

extra="forbid": rechaza campos no definidos en el DTO, como administrador.

Field(min_length=1): impide textos vacíos. Un nombre compuesto solo de espacios también se rechaza después de limpiarlo.

Los nombres y apellidos admiten entre 1 y 100 caracteres. El correo admite entre 1 y 254 caracteres.

En la versión actual, email es de tipo str: se valida su longitud, pero no su formato de correo electrónico. Un texto como "hola" puede ser aceptado. Validar el formato con EmailStr sería una mejora posterior.

El DTO utilizado para los parámetros de consulta contiene:

class EstudianteQueryDTO(BaseModel):
    pagina: int = Field(default=1, ge=1)
    tamano: int = Field(default=10, ge=1, le=100)

Por lo tanto:

pagina debe ser mayor o igual a 1.

tamano debe estar entre 1 y 100.

Si no se indican valores, se utilizan pagina=1 y tamano=10.

DTO, dominio y mapeo

domain/estudiante.py define una entidad con dataclass. No utiliza Pydantic.

El DTO y la entidad de dominio no son lo mismo:

EstudianteCreateDTO
    ↓
    datos recibidos por la API

Estudiante
    ↓
    entidad del dominio

El servicio construye la entidad utilizando los valores recibidos desde el DTO:

estudiante = Estudiante(
    nombre=nombre,
    apellido=apellido,
    email=email,
)

La entidad también ofrece la propiedad nombre_completo y los métodos activar() y desactivar(). Estos dos métodos todavía no tienen endpoints en el router actual.

El DTO de respuesta utiliza:

model_config = ConfigDict(from_attributes=True)

Esto permite leer atributos de un objeto del dominio.

El router realiza la conversión mediante:

EstudianteResponseDTO.model_validate(estudiante)

Pydantic obtiene los atributos correspondientes, valida sus valores y construye el DTO. También puede leer la propiedad nombre_completo.

¿Por qué no existe un mapper?

Por ahora no existe un archivo mapper separado porque la transformación es directa:

DTO
 ↓
Estudiante

y:

Estudiante
 ↓
EstudianteResponseDTO

Agregar un mapper en esta etapa introduciría una abstracción adicional sin resolver un problema real.

Un mapper explícito puede incorporarse posteriormente cuando existan varias representaciones del mismo dato, por ejemplo:

DTO
 ↓
Entidad de dominio
 ↓
Modelo ORM
 ↓
Base de datos

En ese escenario, el mapper se encargaría de transformar una representación en otra.

Mapper y schema no son lo mismo:

Schema: define estructura y validación.

DTO: transporta datos.

Mapper: transforma una representación en otra.

Imports de los DTO

Debido a la nueva estructura, el router debe importar los DTO desde presentation.schemas.dtos.

Los imports correctos son:

from presentation.schemas.dtos.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudiantePaginaDTO,
)

from presentation.schemas.dtos.estudiante_query_dto import (
    EstudianteQueryDTO,
)

No debe utilizarse la ruta antigua:

presentation.dtos

porque esa carpeta ya no forma parte de la estructura actual.

Recorrido de una solicitud

Para crear un estudiante:

Cliente envía POST /estudiantes con JSON
    ↓
FastAPI interpreta la solicitud HTTP
    ↓
EstudianteCreateDTO valida el JSON
    ↓
Router recibe el DTO validado
    ↓
Router pasa los datos al servicio
    ↓
Servicio crea la entidad Estudiante
    ↓
Servicio verifica que el correo no esté duplicado
    ↓
Repositorio asigna un ID
    ↓
Repositorio guarda el estudiante en memoria
    ↓
Servicio devuelve la entidad al router
    ↓
EstudianteResponseDTO.model_validate(estudiante)
    ↓
FastAPI serializa la respuesta a JSON
    ↓
HTTP 201 Created

El dominio no es una parada adicional: define el objeto Estudiante que utilizan el servicio y el repositorio.

Si el DTO rechaza los datos de entrada, FastAPI responde con 422 antes de ejecutar la lógica del servicio.

Endpoints disponibles

Método

Ruta

Acción

Respuesta exitosa

POST

/estudiantes

Crear un estudiante.

201 y estudiante creado.

GET

/estudiantes

Listar con paginación.

200 y página de resultados.

GET

/estudiantes/{estudiante_id}

Consultar por ID.

200 y estudiante.

PUT

/estudiantes/{estudiante_id}

Actualizar nombre, apellido y correo.

200 y estudiante actualizado.

DELETE

/estudiantes/{estudiante_id}

Eliminar el registro de memoria.

204, sin cuerpo.

PUT requiere los tres campos editables; no es una actualización parcial. Conserva el estado activo que ya tenía el estudiante.

DELETE elimina el registro; no llama al método desactivar().

Prueba paso a paso en Swagger

Abre Swagger UI, despliega un endpoint, pulsa Try it out, completa sus datos y pulsa Execute.

1. Crear un estudiante

Usa POST /estudiantes:

{
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com"
}

En una ejecución nueva, el primer estudiante tendrá ID 1.

Respuesta esperada, con código 201:

{
  "id": 1,
  "nombre": "Ana",
  "apellido": "Pérez",
  "email": "ana@example.com",
  "activo": true,
  "nombre_completo": "Ana Pérez"
}

2. Consultar y listar

Consulta el ID devuelto usando:

GET /estudiantes/1

Luego usa:

GET /estudiantes?pagina=1&tamano=5

Si solo creaste el estudiante del ejemplo, recibirás:

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

tamano es el máximo solicitado, no necesariamente la cantidad de elementos recibidos.

total cuenta todos los estudiantes guardados, no solo los de esa página.

3. Actualizar

Usa PUT /estudiantes/1 con:

{
  "nombre": "Ana María",
  "apellido": "Pérez",
  "email": "ana@example.com"
}

Se permite conservar el propio correo.

Si el correo pertenece a otro estudiante, la operación se rechaza.

4. Comprobar validaciones

Prueba

Resultado esperado

Crear con nombre vacío o solo espacios.

422.

Crear agregando un campo administrador.

422.

Crear o actualizar con un correo de otro estudiante.

400.

Listar con pagina=0 o tamano=101.

422.

Consultar, actualizar o eliminar un ID positivo inexistente.

404.

Usar ID 0 o negativo en una ruta de estudiante.

422.

La comparación de correos duplicados ignora mayúsculas y espacios exteriores. Por ejemplo, ANA@example.com y ana@example.com se consideran el mismo correo.

5. Eliminar

Usa:

DELETE /estudiantes/1

Debe responder 204 sin contenido.

Si vuelves a consultar ese ID, debe responder 404.

Cómo funciona la paginación

Ejemplo de solicitud:

GET /estudiantes?pagina=2&tamano=5

EstudianteQueryDTO valida los parámetros.

El servicio calcula:

offset = (pagina - 1) * tamano

El repositorio ordena por ID y selecciona la parte correspondiente de la lista.

El router construye EstudiantePaginaDTO con los resultados y el total.

Con página 2 y tamaño 5:

offset = (2 - 1) * 5
offset = 5

Se saltan los primeros cinco registros y se devuelven hasta cinco más.

Una página fuera de los resultados devuelve:

{
  "items": [],
  "total": 3,
  "pagina": 10,
  "tamano": 5
}

con código 200, conservando el total real.

Consideraciones del almacenamiento en memoria

La versión actual utiliza un repositorio en memoria.

EstudianteRepository
        ↓
dict[int, Estudiante]

Esto implica:

La instancia estudiante_repository se reutiliza entre solicitudes del mismo proceso.

Los datos se pierden cuando el servidor se detiene o reinicia.

Los datos también pueden perderse cuando --reload reinicia el proceso.

No se utiliza una base de datos.

No se utiliza ORM.

No existen migraciones.

No ejecutes este ejemplo con varios workers: cada proceso tendría su propio diccionario.

El repositorio usa copias para evitar que modificar un objeto devuelto cambie accidentalmente el registro almacenado.

La versión didáctica no incorpora bloqueos ni transacciones para solicitudes simultáneas.

No garantiza IDs y correos únicos bajo concurrencia.

No incluye autenticación ni permisos.

No debe exponerse públicamente con datos reales de estudiantes.

Resumen de la arquitectura actual

CLIENTE
   │
   │ HTTP / JSON
   ▼
┌──────────────────────────────┐
│ PRESENTATION                 │
│                              │
│ Router                       │
│   ↓                          │
│ schemas/dtos                 │
│ Pydantic + validaciones      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ APPLICATION                  │
│                              │
│ EstudianteService            │
│ Casos de uso y coordinación  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DOMAIN                       │
│                              │
│ Estudiante                   │
│ Estado y comportamiento      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ INFRASTRUCTURE               │
│                              │
│ EstudianteRepository         │
│ almacenamiento en memoria    │
└──────────────────────────────┘

La dirección principal del flujo es:

HTTP
 ↓
Router
 ↓
DTO / Schema
 ↓
Service
 ↓
Domain
 ↓
Repository
 ↓
Memoria

Problemas frecuentes

No module named 'presentation.dtos'

Después de mover los DTO a schemas/dtos, los imports antiguos dejan de funcionar.

Utiliza:

from presentation.schemas.dtos.estudiante_dto import ...

y:

from presentation.schemas.dtos.estudiante_query_dto import ...

No module named 'app'

Ejecuta el servidor desde la raíz, no desde dentro de app.

En PowerShell puedes comprobarlo con:

Get-Location
Get-ChildItem
Test-Path .\app\main.py

El último comando debe devolver True.

cannot import name 'EstudianteRepository'

Comprueba que el archivo infrastructure/repositories/estudiante_repository.py esté guardado y contenga tanto la clase EstudianteRepository como la instancia:

estudiante_repository = EstudianteRepository()

No aparecen endpoints en Swagger

Comprueba que app/main.py tenga:

from fastapi import FastAPI
from presentation.routers.estudiante_router import router

app = FastAPI(title="Sistema Académico")
app.include_router(router)

Archivos que no deben subirse a Git

El .gitignore debe incluir al menos:

.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.env

Sí debes conservar:

pyproject.toml
uv.lock

Si los archivos __pycache__ ya están publicados, agregar estas reglas no los retira del seguimiento: hace falta quitarlos también del índice de Git.

Estado actual del proyecto

En esta etapa se trabajan los siguientes conceptos:

FastAPI.

Uvicorn.

HTTP y JSON.

Rutas y endpoints.

CRUD.

Pydantic.

DTO.

Schemas.

Validación de entrada y salida.

Separación por capas.

Entidades de dominio.

Servicios.

Repositorios.

Almacenamiento en memoria.

Paginación.

Manejo de errores HTTP.

Swagger / OpenAPI.

Todavía no se incorporan:

Base de datos.

ORM.

Migraciones.

Mapper explícito.

Autenticación.

Autorización.

Docker.

CI/CD.

La incorporación de estas responsabilidades se realizará progresivamente a medida que el proyecto evolucione.