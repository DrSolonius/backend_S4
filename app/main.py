from fastapi import FastAPI

from application.services.estudiante_service import EstudianteService
from infrastructure.repositories.estudiante_repository import (
    estudiante_repository,
)
from infrastructure.seeders.estudiante_seeder import seed_estudiantes
from presentation.routers.estudiante_router import router


app = FastAPI(title="Sistema Académico")

service = EstudianteService(estudiante_repository)

seed_estudiantes(service)

app.include_router(router)