from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image


RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_ASSETS = RAIZ_PROYECTO / "assets"

ICONO_PNG = CARPETA_ASSETS / "icon.png"
ICONO_ICO = CARPETA_ASSETS / "icon.ico"
ICONO_ICNS = CARPETA_ASSETS / "icon.icns"
CARPETA_ICONSET = CARPETA_ASSETS / "icon.iconset"

TAMANOS_MACOS = {
    "icon_16x16.png": 16,
    "icon_16x16@2x.png": 32,
    "icon_32x32.png": 32,
    "icon_32x32@2x.png": 64,
    "icon_128x128.png": 128,
    "icon_128x128@2x.png": 256,
    "icon_256x256.png": 256,
    "icon_256x256@2x.png": 512,
    "icon_512x512.png": 512,
    "icon_512x512@2x.png": 1024,
}

TAMANOS_WINDOWS = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def comprobar_icono_origen() -> None:
    """Comprueba que exista el icono PNG maestro."""
    if not ICONO_PNG.is_file():
        raise FileNotFoundError(
            f"No se encontró el icono maestro: {ICONO_PNG}\n"
            "Guarda una imagen PNG cuadrada de 1024x1024 en assets/icon.png."
        )


def cargar_icono() -> Image.Image:
    """Carga y valida el icono PNG maestro."""
    imagen = Image.open(ICONO_PNG).convert("RGBA")

    if imagen.width != imagen.height:
        raise ValueError("El icono maestro debe ser cuadrado.")

    if imagen.width < 1024:
        raise ValueError(
            "Se recomienda que assets/icon.png tenga al menos 1024x1024 píxeles."
        )

    return imagen


def generar_ico(imagen: Image.Image) -> None:
    """Genera el icono ICO para Windows."""
    imagen.save(
        ICONO_ICO,
        format="ICO",
        sizes=TAMANOS_WINDOWS,
    )
    print(f"Generado: {ICONO_ICO}")


def generar_iconset(imagen: Image.Image) -> None:
    """Genera la carpeta iconset requerida por macOS."""
    if CARPETA_ICONSET.exists():
        shutil.rmtree(CARPETA_ICONSET)

    CARPETA_ICONSET.mkdir(parents=True)

    for nombre, tamano in TAMANOS_MACOS.items():
        destino = CARPETA_ICONSET / nombre
        redimensionada = imagen.resize(
            (tamano, tamano),
            Image.Resampling.LANCZOS,
        )
        redimensionada.save(destino)

    print(f"Generado: {CARPETA_ICONSET}")


def generar_icns() -> None:
    """Genera el icono ICNS usando iconutil en macOS."""
    if sys.platform != "darwin":
        print("ICNS omitido: iconutil solo está disponible en macOS.")
        return

    if shutil.which("iconutil") is None:
        raise RuntimeError("No se encontró el comando iconutil.")

    subprocess.run(
        [
            "iconutil",
            "-c",
            "icns",
            str(CARPETA_ICONSET),
            "-o",
            str(ICONO_ICNS),
        ],
        check=True,
    )

    print(f"Generado: {ICONO_ICNS}")


def limpiar_iconset() -> None:
    """Elimina la carpeta temporal iconset."""
    if CARPETA_ICONSET.exists():
        shutil.rmtree(CARPETA_ICONSET)


def main() -> None:
    """Genera los iconos de macOS y Windows."""
    comprobar_icono_origen()
    imagen = cargar_icono()

    generar_ico(imagen)
    generar_iconset(imagen)

    try:
        generar_icns()
    finally:
        limpiar_iconset()

    print("Iconos generados correctamente.")


if __name__ == "__main__":
    main()
