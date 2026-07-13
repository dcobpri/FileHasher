from pathlib import Path
from threading import Event, Thread

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


from filehasher.controller import FileHasherController
from filehasher.hashing import CalculoCanceladoError


class FileHasherApp:
    """Ventana principal de la aplicación."""

    def __init__(self):
        self.root = tk.Tk()

        self.controller = FileHasherController()
        self.algoritmo = tk.StringVar(value="SHA-256")
        self.progreso = tk.DoubleVar(value=0.0)
        self.evento_cancelacion = Event()
        self.root.title("FileHasher")

        self.root.minsize(700, 480)

        self.crear_widgets()

    def crear_widgets(self) -> None:
        """Construye la interfaz gráfica."""
        etiqueta_archivo = tk.Label(self.root, text="Archivo")
        etiqueta_archivo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_archivo = tk.Entry(self.root, width=50)
        self.entry_archivo.grid(row=0, column=1, padx=10, pady=10)

        self.boton_examinar = tk.Button(
            self.root,
            text="Examinar",
            command=self.seleccionar_archivo,
        )
        self.boton_examinar.grid(row=0, column=2, padx=10, pady=10)

        etiqueta_hash = tk.Label(self.root, text="Hash calculado")
        etiqueta_hash.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_hash = tk.Entry(self.root, width=70)
        self.entry_hash.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
        )

        etiqueta_algoritmo = tk.Label(self.root, text="Algoritmo")
        etiqueta_algoritmo.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w",
        )

        self.combo_algoritmo = ttk.Combobox(
            self.root,
            textvariable=self.algoritmo,
            values=["MD5", "SHA-1", "SHA-256"],
            state="readonly",
            width=15,
        )
        self.combo_algoritmo.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="w",
        )

        self.label_hash_esperado = tk.Label(
            self.root,
            text="Hash esperado",
        )
        self.label_hash_esperado.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w",
        )

        self.entry_hash_esperado = tk.Entry(
            self.root,
            width=70,
        )
        self.entry_hash_esperado.grid(
            row=3,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
        )

        self.boton_verificar = tk.Button(
            self.root,
            text="Verificar",
            command=self.verificar_hash,
            state="disabled",
        )
        self.boton_verificar.grid(
            row=4,
            column=1,
            pady=10,
        )

        self.label_resultado = tk.Label(
            self.root,
            text="",
        )
        self.label_resultado.grid(
            row=5,
            column=1,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w",
        )

        self.barra_progreso = ttk.Progressbar(
            self.root,
            variable=self.progreso,
            maximum=100,
            length=400,
        )
        self.barra_progreso.grid(
            row=6,
            column=1,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="w",
        )

        self.boton_calcular = tk.Button(
            self.root,
            text="Calcular hash",
            command=self.calcular_hash,
        )
        self.boton_calcular.grid(
            row=7,
            column=1,
            pady=10,
        )

        self.boton_cancelar = tk.Button(
            self.root,
            text="Cancelar",
            command=self.cancelar_calculo,
            state="disabled",
        )
        self.boton_cancelar.grid(
            row=7,
            column=2,
            pady=10,
        )

        self.boton_copiar = tk.Button(
            self.root,
            text="Copiar hash",
            command=self.copiar_hash,
        )
        self.boton_copiar.grid(
            row=8,
            column=1,
            pady=10,
        )

    def seleccionar_archivo(self) -> None:
        """Abre un diálogo para seleccionar un archivo."""
        ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo")

        if ruta_archivo:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, ruta_archivo)

    def deshabilitar_controles(self) -> None:
        self.entry_archivo.config(state="disabled")
        self.boton_calcular.config(state="disabled")
        self.boton_examinar.config(state="disabled")
        self.combo_algoritmo.config(state="disabled")
        self.boton_copiar.config(state="disabled")
        self.boton_cancelar.config(state="normal")

    def habilitar_controles(self) -> None:
        self.entry_archivo.config(state="normal")
        self.boton_calcular.config(state="normal")
        self.boton_examinar.config(state="normal")
        self.combo_algoritmo.config(state="readonly")
        self.boton_copiar.config(state="normal")
        self.boton_cancelar.config(state="disabled")

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

        algoritmo = self.algoritmo.get()

        self.entry_hash.delete(0, tk.END)
        self.progreso.set(0.0)

        self.deshabilitar_controles()
        self.evento_cancelacion.clear()
        self.label_resultado.config(text="")
        self.boton_verificar.config(state="disabled")

        hilo = Thread(
            target=self.calcular_hash_worker,
            args=(
                ruta,
                algoritmo,
                self.evento_cancelacion,
            ),
        )

        hilo.start()

    def calcular_hash_worker(
        self,
        ruta: str,
        algoritmo: str,
        evento_cancelacion: Event,
    ) -> None:
        """Calcula el hash en un hilo secundario."""

        try:
            resultado, tiempo = self.controller.calcular_hash(
                ruta,
                algoritmo,
                self.notificar_progreso,
                evento_cancelacion,
            )

            self.root.after(
                0,
                self.mostrar_resultado,
                resultado,
                tiempo,
            )

        except CalculoCanceladoError:
            self.root.after(
                0,
                self.mostrar_cancelacion,
            )

    def mostrar_resultado(self, resultado: str, tiempo: float) -> None:
        """Muestra el resultado del cálculo en la interfaz."""
        self.progreso.set(100.0)

        self.entry_hash.delete(0, tk.END)
        self.entry_hash.insert(0, resultado)
        self.boton_verificar.config(state="normal")

        mensaje = (
            f"Hash {self.algoritmo.get()} calculado correctamente.\n\n"
            f"Tiempo empleado: {tiempo:.3f} segundos."
        )

        self.habilitar_controles()
        messagebox.showinfo("Hash calculado", mensaje)

    def actualizar_progreso(self, procesados: int, totales: int) -> None:
        """Actualiza la barra de progreso."""
        if totales == 0:
            porcentaje = 100.0
        else:
            porcentaje = procesados / totales * 100

        self.progreso.set(porcentaje)

    def notificar_progreso(self, procesados: int, totales: int) -> None:
        """Solicita al hilo principal actualizar el progreso."""

        self.root.after(
            0,
            self.actualizar_progreso,
            procesados,
            totales,
        )

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

    def mostrar_cancelacion(self) -> None:
        """Muestra que el cálculo fue cancelado."""
        self.entry_hash.delete(0, tk.END)
        self.entry_hash.insert(0, "Cancelado")

        self.habilitar_controles()

        messagebox.showinfo(
            "Cálculo cancelado",
            "El cálculo del hash se ha cancelado correctamente.",
        )

    def cancelar_calculo(self) -> None:
        """Solicita la cancelación del cálculo."""
        self.evento_cancelacion.set()

    def verificar_hash(self) -> None:
        """Verifica si el hash calculado coincide con el esperado."""
        hash_calculado = self.entry_hash.get().strip()
        hash_esperado = self.entry_hash_esperado.get().strip()

        if not hash_calculado:
            messagebox.showwarning(
                "Hash no disponible",
                "Calcula primero el hash de un archivo.",
            )
            return

        if not hash_esperado:
            messagebox.showwarning(
                "Hash esperado vacío",
                "Introduce el hash esperado antes de verificar.",
            )
            return

        coincide = self.controller.verificar_hash(
            hash_calculado,
            hash_esperado,
        )

        if coincide:
            self.label_resultado.config(
                text="Coincide",
                fg="green",
            )
        else:
            self.label_resultado.config(
                text="No coincide",
                fg="red",
            )

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
