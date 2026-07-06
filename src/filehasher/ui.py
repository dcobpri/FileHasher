import tkinter as tk
from tkinter import filedialog, messagebox

from filehasher.hashing import calcular_sha256


class FileHasherApp:
    """Ventana principal de la aplicación."""

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("FileHasher")

        self.root.geometry("600x250")

        self.crear_widgets()

    def crear_widgets(self):
        """Construye la interfaz gráfica."""
        etiqueta_archivo = tk.Label(self.root, text="Archivo")
        etiqueta_archivo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_archivo = tk.Entry(self.root, width=50)
        self.entry_archivo.grid(row=0, column=1, padx=10, pady=10)

        self.boton_examinar = tk.Button(
            self.root,
            text="Examinar",
            command=self.seleccionar_archivo
        )
        self.boton_examinar.grid(row=0, column=2, padx=10, pady=10)

        etiqueta_hash = tk.Label(self.root, text="SHA-256")
        etiqueta_hash.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_hash = tk.Entry(self.root, width=70)
        self.entry_hash.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        self.boton_calcular = tk.Button(
            self.root,
            text="Calcular hash",
            command=self.calcular_hash
        )
        self.boton_calcular.grid(row=2, column=1, pady=20)

    def seleccionar_archivo(self) -> None:
        """Abre un diálogo para seleccionar un archivo."""
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo"
        )

        if ruta_archivo:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, ruta_archivo)
    
    def calcular_hash(self) -> None:
        """Calcula el hash del archivo seleccionado."""

        ruta = self.entry_archivo.get()

        if not ruta:
            messagebox.showwarning(
                "Archivo no seleccionado",
                "Selecciona un archivo antes de calcular el hash."
            )
            return

        resultado = calcular_sha256(ruta)

        self.entry_hash.delete(0, tk.END)
        self.entry_hash.insert(0, resultado)

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
