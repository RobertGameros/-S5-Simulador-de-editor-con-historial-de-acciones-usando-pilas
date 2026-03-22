# stack.py

class Stack:
    """
    Implementación propia de una Pila (LIFO).
    Imagina una pila de platos: el último plato que pones arriba,
    es el primero que tienes que quitar.
    """

    def __init__(self):
        # Usamos una lista normal de Python para guardar los datos,
        # pero la ocultamos para controlarla con nuestras propias reglas.
        self._items = []

    def push(self, item):
        """Agrega un elemento a la cima de la pila."""
        self._items.append(item)

    def pop(self):
        """Saca y te entrega el último elemento que se agregó."""
        if self.is_empty():
            return None # Si no hay nada, no devuelve nada (evita errores)
        return self._items.pop()

    def peek(self):
        """Solo mira cuál es el elemento de arriba, pero no lo saca."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        """Nos dice si la pila está vacía (True) o tiene algo (False)."""
        return len(self._items) == 0

    def size(self):
        """Nos dice cuántos elementos hay guardados en total."""
        return len(self._items)

    def clear(self):
        """Limpia la pila por completo, dejándola como nueva."""
        self._items = []