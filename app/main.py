from fastapi import FastAPI

from presentation.routers.estudiante_router import router


app = FastAPI(title="Sistema Académico")

app.include_router(router)