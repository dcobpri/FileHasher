from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    """
    Devuelve la ruta absoluta de un recurso tanto en desarrollo
    como cuando la aplicación está empaquetada con PyInstaller.
    """
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path
