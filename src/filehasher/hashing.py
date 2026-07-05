"""
Funciones relacionadas con el cálculo de hashes criptográficos.
"""

from pathlib import Path
import hashlib


def calcular_sha256(ruta_archivo: str) -> str:
    """
    Calcula el hash SHA-256 de un archivo.

    Parameters
    ----------
    ruta_archivo : str
        Ruta del archivo cuyo hash se desea calcular.

    Returns
    -------
    str
        Hash SHA-256 en formato hexadecimal.
    """

    ruta = Path(ruta_archivo)

    with ruta.open("rb") as archivo:
        contenido = archivo.read()

    return hashlib.sha256(contenido).hexdigest()
