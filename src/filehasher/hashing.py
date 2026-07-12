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
TAMANO_BLOQUE = 65536

ProgresoCallback = Callable[[int, int], None]


def calcular_hash(
    ruta_archivo: str,
    algoritmo: str,
    progreso: ProgresoCallback | None = None,
) -> str:
    """Calcula el hash de un archivo usando el algoritmo indicado."""
    funcion_hash = ALGORITMOS[algoritmo]
    objeto_hash = funcion_hash()

    ruta = Path(ruta_archivo)
    bytes_totales = ruta.stat().st_size
    bytes_procesados = 0

    for bloque in leer_bloques(ruta_archivo):
        objeto_hash.update(bloque)

        bytes_procesados += len(bloque)

        if progreso is not None:
            progreso(bytes_procesados, bytes_totales)

    return objeto_hash.hexdigest()


def calcular_sha256(ruta_archivo: str) -> str:
    """
    Calcula el hash SHA-256 de un archivo.
    """
    return calcular_hash(ruta_archivo, "SHA-256")


def leer_bloques(ruta_archivo: str):
    """Lee un archivo por bloques."""
    ruta = Path(ruta_archivo)

    with ruta.open("rb") as archivo:
        while True:
            bloque = archivo.read(TAMANO_BLOQUE)

            if not bloque:
                break

            yield bloque
