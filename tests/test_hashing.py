from pathlib import Path

from filehasher.hashing import calcular_sha256


def test_sha256(tmp_path: Path) -> None:
    """
    Comprueba que calcular_sha256 devuelve el hash correcto.
    """

    archivo = tmp_path / "prueba.txt"

    archivo.write_text("Hola Mundo", encoding="utf-8")

    resultado = calcular_sha256(str(archivo))

    esperado = "c3a4a2e49d91f2177113a9adfcb9ef9af9679dc4557a0a3a4602e1bd39a6f481"

    assert resultado == esperado
