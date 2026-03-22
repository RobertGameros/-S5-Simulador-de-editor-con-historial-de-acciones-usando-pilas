# editor.py
from stack import Stack

class TextEditor:
    """
    El 'cerebro' de nuestro editor. Aquí no hay botones ni colores,
    solo la lógica de cómo se procesa el texto y el historial.
    """

    def __init__(self):
        self.content = "" # Aquí se guarda el texto actual
        self.undo_stack = Stack() # Pila para guardar lo que podemos deshacer
        self.redo_stack = Stack() # Pila para guardar lo que podemos rehacer
        self.action_history = []  # Lista simple para mostrar el historial en pantalla

    def _log_history(self, action_str):
        """Anota cada paso que da el usuario para mostrarlo en el historial."""
        self.action_history.append(action_str)

    def write(self, text):
        """Agrega texto nuevo al documento."""
        if not text:
            raise ValueError("No se puede escribir texto vacío.")

        self.content += text

        # Guardamos qué hicimos para poder deshacerlo después
        self.undo_stack.push({"action": "write", "text": text})

        # Si escribimos algo nuevo, el futuro cambia, así que limpiamos la pila de rehacer
        self.redo_stack.clear()
        self._log_history(f"Escribió: '{text}'")

    def delete(self, n):
        """Borra una cantidad específica de letras del final."""
        if n <= 0:
            raise ValueError("Debe borrar al menos 1 carácter.")

        # Si nos piden borrar 10 letras pero solo hay 3, ajustamos para no causar un error
        if n > len(self.content):
            n = len(self.content)

        if n == 0:
            return # Si no hay nada que borrar, no hacemos nada

        # Separamos el texto que se va a borrar del que se queda
        deleted_text = self.content[-n:]
        self.content = self.content[:-n]

        # Guardamos qué borramos para poder recuperarlo si el usuario hace "Deshacer"
        self.undo_stack.push({"action": "delete", "text": deleted_text})
        self.redo_stack.clear()
        self._log_history(f"Borró: '{deleted_text}' ({n} caracteres)")

    def undo(self):
        """Deshace el último paso del usuario."""
        if self.undo_stack.is_empty():
            raise IndexError("No hay acciones para deshacer.")

        last_action = self.undo_stack.pop() # Sacamos la última acción de la pila

        # Hacemos exactamente lo contrario a la acción original
        if last_action["action"] == "write":
            # Si escribió, lo deshacemos borrando
            length = len(last_action["text"])
            self.content = self.content[:-length]
        elif last_action["action"] == "delete":
            # Si borró, lo deshacemos volviendo a escribir
            self.content += last_action["text"]

        # Pasamos esta acción a la pila de "Rehacer" por si el usuario cambia de opinión
        self.redo_stack.push(last_action)
        self._log_history(f"Deshizo: {last_action['action']}")

    def redo(self):
        """Vuelve a aplicar un paso que el usuario había deshecho."""
        if self.redo_stack.is_empty():
            raise IndexError("No hay acciones para rehacer.")

        action = self.redo_stack.pop()

        # Volvemos a ejecutar la acción original
        if action["action"] == "write":
            self.content += action["text"]
        elif action["action"] == "delete":
            length = len(action["text"])
            self.content = self.content[:-length]

        # Lo devolvemos a la pila de deshacer para mantener el ciclo vivo
        self.undo_stack.push(action)
        self._log_history(f"Rehizo: {action['action']}")

    def show(self):
        """Devuelve el texto actual para que la interfaz lo pueda dibujar."""
        return self.content

    def history(self):
        """Devuelve la lista del historial completo."""
        return self.action_history