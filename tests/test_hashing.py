from pathlib import Path
from threading import Event

import pytest

from filehasher.hashing import (
    CalculoCanceladoError,
    calcular_hash,
    calcular_sha256,
)


def test_sha256(tmp_path: Path) -> None:
    """
    Comprueba que calcular_sha256 devuelve el hash correcto.
    """

    archivo = tmp_path / "prueba.txt"

    archivo.write_text("Hola Mundo", encoding="utf-8")

    resultado = calcular_sha256(str(archivo))

    esperado = "c3a4a2e49d91f2177113a9adfcb9ef9af9679dc4557a0a3a4602e1bd39a6f481"

    assert resultado == esperado


def test_md5(tmp_path: Path) -> None:
    archivo = tmp_path / "archivo.txt"
    archivo.write_text("Hola", encoding="utf-8")

    resultado = calcular_hash(str(archivo), "MD5")

    esperado = "f688ae26e9cfa3ba6235477831d5122e"

    assert resultado == esperado


def test_sha1(tmp_path: Path) -> None:
    archivo = tmp_path / "archivo.txt"
    archivo.write_text("Hola", encoding="utf-8")

    resultado = calcular_hash(str(archivo), "SHA-1")

    esperado = "4e46dc0969e6621f2d61d2228e3cd91b75cd9edc"

    assert resultado == esperado


def test_archivo_vacio(tmp_path: Path) -> None:
    archivo = tmp_path / "vacio.txt"
    archivo.write_bytes(b"")

    resultado = calcular_hash(str(archivo), "SHA-256")

    esperado = "e3b0c44298fc1c149afbf4c8996fb924" "27ae41e4649b934ca495991b7852b855"

    assert resultado == esperado


def test_algoritmo_no_soportado(tmp_path: Path) -> None:
    archivo = tmp_path / "archivo.txt"
    archivo.write_text("Hola", encoding="utf-8")

    with pytest.raises(KeyError):
        calcular_hash(str(archivo), "SHA-999")


def test_cancelacion(tmp_path: Path) -> None:
    archivo = tmp_path / "archivo_grande.bin"
    archivo.write_bytes(b"a" * 200_000)

    evento = Event()
    evento.set()

    with pytest.raises(CalculoCanceladoError):
        calcular_hash(
            str(archivo),
            "SHA-256",
            evento_cancelacion=evento,
        )
