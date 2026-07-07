"""
Controlador de la aplicación FileHasher.
"""

from filehasher import hashing


class FileHasherController:
    """Coordina la lógica de la aplicación."""

    def calcular_hash(self, ruta: str, algoritmo: str) -> str:
        """
        Calcula el hash de un archivo usando el algoritmo indicado.
        """
        return hashing.calcular_hash(ruta, algoritmo)
