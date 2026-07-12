"""
Controlador de la aplicación FileHasher.
"""

from time import perf_counter

from filehasher import hashing
from filehasher.hashing import ProgresoCallback


class FileHasherController:
    """Coordina la lógica de la aplicación."""

    def calcular_hash(
        self,
        ruta: str,
        algoritmo: str,
        progreso: ProgresoCallback | None = None,
    ) -> tuple[str, float]:
        """
        Calcula el hash de un archivo usando el algoritmo indicado.

        Returns
        -------
        tuple[str, float]
            Hash calculado y tiempo empleado en segundos.
        """
        inicio = perf_counter()

        resultado = hashing.calcular_hash(
            ruta,
            algoritmo,
            progreso,
        )

        fin = perf_counter()

        return resultado, fin - inicio
