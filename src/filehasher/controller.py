"""
Controlador de la aplicación FileHasher.
"""

from time import perf_counter
from threading import Event

from filehasher import hashing
from filehasher.hashing import ProgresoCallback


class FileHasherController:
    """Coordina la lógica de la aplicación."""

    def calcular_hash(
        self,
        ruta: str,
        algoritmo: str,
        progreso: ProgresoCallback | None = None,
        evento_cancelacion: Event | None = None,
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
            evento_cancelacion,
        )

        fin = perf_counter()

        return resultado, fin - inicio

    def verificar_hash(self, calculado: str, esperado: str) -> bool:
        """Comprueba si dos hashes coinciden."""
        calculado_normalizado = calculado.strip().lower()
        esperado_normalizado = esperado.strip().lower()

        return calculado_normalizado == esperado_normalizado
