from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from filehasher.controller import FileHasherController


class FileHasherApp:
    """Ventana principal de la aplicación."""

    def __init__(self):
        self.root = tk.Tk()

        self.controller = FileHasherController()
        self.algoritmo = tk.StringVar(value="SHA-256")
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
            self.root, text="Examinar", command=self.seleccionar_archivo
        )
        self.boton_examinar.grid(row=0, column=2, padx=10, pady=10)

        etiqueta_hash = tk.Label(self.root, text="SHA-256")
        etiqueta_hash.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_hash = tk.Entry(self.root, width=70)
        self.entry_hash.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        etiqueta_algoritmo = tk.Label(self.root, text="Algoritmo")

        etiqueta_algoritmo.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.combo_algoritmo = ttk.Combobox(
            self.root,
            textvariable=self.algoritmo,
            values=["MD5", "SHA-1", "SHA-256"],
            state="readonly",
            width=15,
        )

        self.combo_algoritmo.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.boton_calcular = tk.Button(
            self.root, text="Calcular hash", command=self.calcular_hash
        )
        self.boton_calcular.grid(row=3, column=1, pady=20)

        self.boton_copiar = tk.Button(
            self.root,
            text="Copiar hash",
            command=self.copiar_hash,
        )

        self.boton_copiar.grid(
            row=4,
            column=1,
            pady=10,
        )

    def seleccionar_archivo(self) -> None:
        """Abre un diálogo para seleccionar un archivo."""
        ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo")

        if ruta_archivo:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, ruta_archivo)

    def calcular_hash(self) -> None:
        """Calcula el hash del archivo seleccionado."""

        ruta = self.entry_archivo.get()

        if not ruta:
            messagebox.showwarning(
                "Archivo no seleccionado",
                "Selecciona un archivo antes de calcular el hash.",
            )
            return

        if not Path(ruta).is_file():
            messagebox.showerror(
                "Ruta no válida", "La ruta seleccionada no corresponde a un archivo."
            )
            return

        resultado = self.controller.calcular_hash(
            ruta,
            self.algoritmo.get(),
        )
        self.entry_hash.delete(0, tk.END)
        self.entry_hash.insert(0, resultado)

    def copiar_hash(self) -> None:
        """Copia el hash al portapapeles."""
        hash_texto = self.entry_hash.get().strip()
        metodo_hash = self.algoritmo.get()

        if not hash_texto:
            messagebox.showwarning(
                "Hash no disponible",
                "Calcula primero el hash de un archivo antes de copiarlo.",
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(hash_texto)

        mensaje = f"Hash {metodo_hash} copiado al portapapeles."
        messagebox.showinfo("Hash copiado", mensaje)

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
