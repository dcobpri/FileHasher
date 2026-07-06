import tkinter as tk


class FileHasherApp:
    """Ventana principal de la aplicación."""

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("FileHasher")

        self.root.geometry("600x250")

        self.crear_widgets()

    def crear_widgets(self):
        """Construye la interfaz gráfica."""
        pass

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
