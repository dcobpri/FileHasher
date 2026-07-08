"""
Funciones relacionadas con el cálculo de hashes criptográficos.
"""

from collections.abc import Callable
from pathlib import Path
import hashlib

ALGORITMOS: dict[str, Callable] = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256,
}


def calcular_hash(ruta_archivo: str, algoritmo: str) -> str:
    """
    Calcula el hash de un archivo usando el algoritmo indicado.
    """

    funcion_hash = ALGORITMOS[algoritmo]
    objeto_hash = funcion_hash()

    ruta = Path(ruta_archivo)

    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(65536), b""):
            objeto_hash.update(bloque)

    return objeto_hash.hexdigest()


def calcular_sha256(ruta_archivo: str) -> str:
    """
    Calcula el hash SHA-256 de un archivo.
    """
    return calcular_hash(ruta_archivo, "SHA-256")
