# ui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from editor import TextEditor

class EditorUI:
    """
    La 'cara' del programa. Aquí dibujamos la ventana, los colores
    y conectamos los clics del usuario con el 'cerebro' (TextEditor).
    """
    def __init__(self, root):
        self.editor = TextEditor() # Conectamos la interfaz con la lógica
        self.root = root

        # Configuración inicial de la ventana
        self.root.title("Simulador de Editor de Texto (LIFO Stack)")
        self.root.geometry("750x500")
        self.root.configure(bg="#F5F7FA")
        self.root.minsize(700, 480)

        self._build_ui()
        self._update_display()

    @staticmethod
    def _create_hover_effect(widget, color_normal, color_hover):
        """Un pequeño truco visual para que los botones cambien de color al pasar el mouse."""
        widget.bind("<Enter>", lambda e: widget.config(bg=color_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=color_normal))

    def _build_ui(self):
        """Construye y acomoda todas las piezas (botones, cuadros de texto) en la pantalla."""

        # Marco principal que sostiene todo
        main_frame = tk.Frame(self.root, bg="#F5F7FA", padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)

        # Configuramos cómo se reparten los espacios (izquierda vs derecha)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=0) # Separador
        main_frame.columnconfigure(2, weight=2) # Área de historial
        main_frame.rowconfigure(0, weight=1)

        # --- Zona Izquierda: Donde el usuario escribe y hace clic ---
        left_frame = tk.Frame(main_frame, bg="#F5F7FA")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        # Encabezado con el título y el botón de instrucciones
        header_frame = tk.Frame(left_frame, bg="#F5F7FA")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)

        tk.Label(header_frame, text="Contenido Actual:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#2C3E50").grid(row=0, column=0, sticky="w")

        btn_info = tk.Button(header_frame, text="ℹ️ Instrucciones", command=self.show_instructions, bg="#95A5A6", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2")
        btn_info.grid(row=0, column=1, sticky="e", ipadx=10, ipady=3)
        self._create_hover_effect(btn_info, "#95A5A6", "#BDC3C7")

        # El "papel" blanco donde se muestra el texto final (está bloqueado para que no escriban directo)
        self.text_display = tk.Text(left_frame, height=6, width=40, state="disabled", font=("Consolas", 12), bg="#FFFFFF", fg="#34495E", relief="flat", padx=10, pady=10)
        self.text_display.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

        # --- Zona de Botones ---
        control_frame = tk.Frame(left_frame, bg="#F5F7FA")
        control_frame.grid(row=2, column=0, sticky="nsew")
        control_frame.columnconfigure(0, weight=2)
        control_frame.columnconfigure(1, weight=1)

        # Caja para escribir y su botón verde
        self.entry_write = tk.Entry(control_frame, font=("Segoe UI", 11), relief="flat")
        self.entry_write.grid(row=0, column=0, padx=(0, 10), pady=8, sticky="ew", ipady=5)
        self.entry_write.bind("<Return>", lambda e: self.handle_write()) # Permite usar la tecla Enter

        btn_write = tk.Button(control_frame, text="Escribir", command=self.handle_write, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_write.grid(row=0, column=1, pady=8, ipadx=10, ipady=3, sticky="ew")
        self._create_hover_effect(btn_write, "#4CAF50", "#45A049")

        # Caja para borrar y su botón rojo
        self.entry_delete = tk.Entry(control_frame, font=("Segoe UI", 11), relief="flat", justify="center")
        self.entry_delete.grid(row=1, column=0, padx=(0, 10), pady=8, sticky="ew", ipady=5)
        self.entry_delete.bind("<Return>", lambda e: self.handle_delete())

        btn_delete = tk.Button(control_frame, text="Borrar (N carac.)", command=self.handle_delete, bg="#FF6B6B", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_delete.grid(row=1, column=1, pady=8, ipadx=10, ipady=3, sticky="ew")
        self._create_hover_effect(btn_delete, "#FF6B6B", "#FF5252")

        # Botones de Deshacer (Amarillo) y Rehacer (Azul)
        undo_redo_frame = tk.Frame(control_frame, bg="#F5F7FA")
        undo_redo_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        undo_redo_frame.columnconfigure(0, weight=1)
        undo_redo_frame.columnconfigure(1, weight=1)

        btn_undo = tk.Button(undo_redo_frame, text="⟲ Deshacer", command=self.handle_undo, bg="#FFB300", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_undo.grid(row=0, column=0, padx=(0, 5), ipadx=10, ipady=5, sticky="ew")
        self._create_hover_effect(btn_undo, "#FFB300", "#FFCA28")

        btn_redo = tk.Button(undo_redo_frame, text="Rehacer ⟳", command=self.handle_redo, bg="#29B6F6", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_redo.grid(row=0, column=1, padx=(5, 0), ipadx=10, ipady=5, sticky="ew")
        self._create_hover_effect(btn_redo, "#29B6F6", "#4FC3F7")

        # --- Separador Visual ---
        separator = ttk.Separator(main_frame, orient="vertical")
        separator.grid(row=0, column=1, sticky="ns", padx=25)

        # --- Zona Derecha: El Historial ---
        right_frame = tk.Frame(main_frame, bg="#F5F7FA")
        right_frame.grid(row=0, column=2, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        tk.Label(right_frame, text="Historial de Acciones:", font=("Segoe UI", 12, "bold"), bg="#F5F7FA", fg="#2C3E50").grid(row=0, column=0, sticky="w", pady=(0, 10))

        history_container = tk.Frame(right_frame, bg="#D1D8E0", bd=1)
        history_container.grid(row=1, column=0, sticky="nsew")

        self.history_display = tk.Listbox(history_container, font=("Segoe UI", 10), bg="#FFFFFF", fg="#34495E", relief="flat")
        self.history_display.pack(side="left", fill="both", expand=True)

        # Le ponemos una barrita para poder bajar y subir por el historial
        scrollbar = ttk.Scrollbar(history_container, orient="vertical", command=self.history_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_display.config(yscrollcommand=scrollbar.set)

    def show_instructions(self):
        """Crea y muestra la ventana emergente de ayuda."""
        info_window = tk.Toplevel(self.root)
        info_window.title("Instrucciones de Uso")
        info_window.geometry("600x520")
        info_window.configure(bg="#FFFFFF")
        info_window.resizable(False, False)

        # Bloquea la ventana principal hasta que cierren esta
        info_window.transient(self.root)
        info_window.grab_set()

        tk.Label(info_window, text="📖 Guía del Editor LIFO", font=("Segoe UI", 16, "bold"), bg="#FFFFFF", fg="#2C3E50").pack(pady=(25, 15))

        instructions_text = (
            "Bienvenido al Simulador de Editor de Texto. Aquí tienes el detalle de cada función:\n\n"
            "🟢 Escribir:\n   Añade el texto al final del documento.\n\n"
            "🔴 Borrar (N carac.):\n   Elimina la cantidad exacta de letras que le pidas.\n\n"
            "🟠 Deshacer (Undo):\n   Usa la Pila (LIFO) para revertir tu último paso.\n\n"
            "🔵 Rehacer (Redo):\n   Vuelve a aplicar un paso que habías deshecho.\n\n"
            "📋 Historial de Acciones:\n   Muestra tu bitácora de todo lo que has hecho."
        )

        tk.Label(info_window, text=instructions_text, font=("Segoe UI", 11), bg="#FFFFFF", justify="left", wraplength=520).pack(padx=35, pady=5, anchor="w")

        btn_close = tk.Button(info_window, text="Entendido", command=info_window.destroy, bg="#4A90E2", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        btn_close.pack(side="bottom", pady=25, ipadx=30, ipady=6)
        self._create_hover_effect(btn_close, "#4A90E2", "#5D9CEC")

    def _update_display(self):
        """Refresca la pantalla tomando los datos más recientes del 'cerebro'."""
        # Refrescar texto principal
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, self.editor.show())
        self.text_display.config(state="disabled")

        # Refrescar historial
        self.history_display.delete(0, tk.END)
        for action in self.editor.history():
            self.history_display.insert(tk.END, action)

        # Hace que la lista siempre muestre lo más reciente abajo
        self.history_display.yview(tk.END)

    # --- Funciones que conectan los botones con el editor ---
    def handle_write(self):
        text = self.entry_write.get()
        if not text:
            return
        try:
            self.editor.write(text) # Mandamos la orden al cerebro
            self.entry_write.delete(0, tk.END) # Limpiamos la cajita
            self._update_display() # Dibujamos el resultado
        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def handle_delete(self):
        try:
            n = int(self.entry_delete.get())
            self.editor.delete(n)
            self.entry_delete.delete(0, tk.END)
            self._update_display()
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un número válido para borrar.")
        except Exception as e:
            messagebox.showwarning("Error", str(e))

    def handle_undo(self):
        try:
            self.editor.undo()
            self._update_display()
        except IndexError as e:
            messagebox.showinfo("Aviso", str(e)) # Si no hay nada que deshacer, avisa sin romper el programa

    def handle_redo(self):
        try:
            self.editor.redo()
            self._update_display()
        except IndexError as e:
            messagebox.showinfo("Aviso", str(e))

# Esto enciende el motor de la interfaz si ejecutamos este archivo directamente
if __name__ == "__main__":
    root = tk.Tk()
    app = EditorUI(root)
    root.mainloop()