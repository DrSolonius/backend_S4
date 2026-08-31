from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from application.services.estudiante_service import EstudianteService
from infrastructure.repositories.estudiante_repository import (
    estudiante_repository,
)
from presentation.schemas.dtos.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudiantePaginaDTO,
)

from presentation.schemas.dtos.estudiante_query_dto import (
    EstudianteQueryDTO,
)


router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"],
)

# Reutilizamos el mismo repositorio en memoria.
service = EstudianteService(estudiante_repository)

EstudianteId = Annotated[int, Path(gt=0)]


@router.post(
    "",
    response_model=EstudianteResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def crear_estudiante(datos: EstudianteCreateDTO):
    try:
        estudiante = service.crear(
            nombre=datos.nombre,
            apellido=datos.apellido,
            email=datos.email,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return EstudianteResponseDTO.model_validate(estudiante)


@router.get("", response_model=EstudiantePaginaDTO)
def listar_estudiantes(
    query: Annotated[EstudianteQueryDTO, Query()],
):
    estudiantes, total = service.listar(
        pagina=query.pagina,
        tamano=query.tamano,
    )

    return EstudiantePaginaDTO(
        items=[
            EstudianteResponseDTO.model_validate(estudiante)
            for estudiante in estudiantes
        ],
        total=total,
        pagina=query.pagina,
        tamano=query.tamano,
    )


@router.get(
    "/{estudiante_id}",
    response_model=EstudianteResponseDTO,
)
def obtener_estudiante(estudiante_id: EstudianteId):
    estudiante = service.obtener(estudiante_id)

    if estudiante is None:
        raise HTTPException(
            status_code=404,
            detail="El estudiante no existe.",
        )

    return EstudianteResponseDTO.model_validate(estudiante)


@router.put(
    "/{estudiante_id}",
    response_model=EstudianteResponseDTO,
)
def actualizar_estudiante(
    estudiante_id: EstudianteId,
    datos: EstudianteUpdateDTO,
):
    try:
        estudiante = service.actualizar(
            estudiante_id=estudiante_id,
            nombre=datos.nombre,
            apellido=datos.apellido,
            email=datos.email,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if estudiante is None:
        raise HTTPException(
            status_code=404,
            detail="El estudiante no existe.",
        )

    return EstudianteResponseDTO.model_validate(estudiante)


@router.delete(
    "/{estudiante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_estudiante(estudiante_id: EstudianteId):
    eliminado = service.eliminar(estudiante_id)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="El estudiante no existe.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)