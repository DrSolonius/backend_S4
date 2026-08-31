from copy import deepcopy
from domain.estudiante import Estudiante
    

class EstudianteRepository:
    def __init__(self) -> None:
        self._estudiantes: dict[int, Estudiante] = {}
        self._siguiente_id = 1

    def crear(self, estudiante: Estudiante) -> Estudiante:
        nuevo = deepcopy(estudiante)
        nuevo.id = self._siguiente_id

        self._estudiantes[nuevo.id] = nuevo
        self._siguiente_id += 1

        return deepcopy(nuevo)

    def obtener_por_id(self, estudiante_id: int) -> Estudiante | None:
        estudiante = self._estudiantes.get(estudiante_id)
        return deepcopy(estudiante)

    def obtener_por_email(self, email: str) -> Estudiante | None:
        email_buscado = email.strip().lower()

        for estudiante in self._estudiantes.values():
            if estudiante.email.strip().lower() == email_buscado:
                return deepcopy(estudiante)

        return None

    def listar(self, offset: int, limite: int) -> list[Estudiante]:
        estudiantes = sorted(
            self._estudiantes.values(),
            key=lambda estudiante: estudiante.id,
        )

        return deepcopy(estudiantes[offset : offset + limite])

    def contar(self) -> int:
        return len(self._estudiantes)

    def actualizar(self, estudiante: Estudiante) -> Estudiante:
        if estudiante.id not in self._estudiantes:
            raise ValueError("El estudiante no existe.")

        self._estudiantes[estudiante.id] = deepcopy(estudiante)
        return deepcopy(estudiante)

    def eliminar(self, estudiante_id: int) -> bool:
        if estudiante_id not in self._estudiantes:
            return False

        del self._estudiantes[estudiante_id]
        return True


# Una sola instancia para compartir los datos entre solicitudes.
estudiante_repository = EstudianteRepository()