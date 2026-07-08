"""
Controlador de la aplicación FileHasher.
"""

from time import perf_counter

from filehasher import hashing


class FileHasherController:
    """Coordina la lógica de la aplicación."""

    def calcular_hash(self, ruta: str, algoritmo: str) -> tuple[str, float]:
        """
        Calcula el hash de un archivo usando el algoritmo indicado.

        Returns
        -------
        tuple[str, float]
            Hash calculado y tiempo empleado en segundos.
        """
        inicio = perf_counter()

        resultado = hashing.calcular_hash(ruta, algoritmo)

        fin = perf_counter()

        return resultado, fin - inicio
