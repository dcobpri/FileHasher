"""
Controlador de la aplicación FileHasher.
"""

from filehasher.hashing import calcular_sha256


class FileHasherController:
    """Coordina la lógica de la aplicación."""

    def calcular_sha256(self, ruta: str) -> str:
        """
        Calcula el hash SHA-256 de un archivo.

        Parameters
        ----------
        ruta : str
            Ruta del archivo.

        Returns
        -------
        str
            Hash SHA-256.
        """

        return calcular_sha256(ruta)
