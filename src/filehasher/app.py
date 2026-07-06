"""
Punto de entrada de la aplicación FileHasher.
"""

from filehasher.ui import FileHasherApp


def main() -> None:
    """Arranca la aplicación."""
    app = FileHasherApp()
    app.run()


if __name__ == "__main__":
    main()
