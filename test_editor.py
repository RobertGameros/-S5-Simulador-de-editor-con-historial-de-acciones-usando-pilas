# test_editor.py
import unittest
from stack import Stack
from editor import TextEditor

class TestStack(unittest.TestCase):
    """Pruebas automáticas para asegurarnos de que la Pila no se equivoque."""
    def test_stack_operations(self):
        s = Stack()
        self.assertTrue(s.is_empty()) # Debe iniciar vacía
        s.push(1)
        s.push(2)
        self.assertEqual(s.size(), 2) # Revisamos que haya contado bien
        self.assertEqual(s.peek(), 2) # El último en entrar fue el 2
        self.assertEqual(s.pop(), 2)  # El primero en salir debe ser el 2
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.pop(), 1)
        self.assertIsNone(s.pop())    # Si sacamos de una pila vacía, no debe explotar

class TestTextEditor(unittest.TestCase):
    """Pruebas automáticas para el 'cerebro' del editor."""
    def setUp(self):
        # Esto se ejecuta antes de cada prueba para tener un editor limpio
        self.editor = TextEditor()

    def test_write_and_show(self):
        self.editor.write("Hola")
        self.assertEqual(self.editor.show(), "Hola")

    def test_write_empty(self):
        # Probamos que el programa se queje si intentamos guardar nada
        with self.assertRaises(ValueError):
            self.editor.write("")

    def test_delete(self):
        self.editor.write("Hola Mundo")
        self.editor.delete(6) # Borramos la palabra " Mundo"
        self.assertEqual(self.editor.show(), "Hola")

    def test_delete_more_than_exists(self):
        self.editor.write("A")
        self.editor.delete(10) # Intentamos borrar 10, pero solo hay 1.
        self.assertEqual(self.editor.show(), "") # El programa debe saber manejarlo y quedar vacío

    def test_undo_redo(self):
        # Probamos la magia del viaje en el tiempo
        self.editor.write("Hola")
        self.editor.write(" Mundo")
        self.assertEqual(self.editor.show(), "Hola Mundo")

        self.editor.undo() # Retrocedemos un paso
        self.assertEqual(self.editor.show(), "Hola")

        self.editor.redo() # Avanzamos de nuevo
        self.assertEqual(self.editor.show(), "Hola Mundo")

    def test_undo_empty(self):
        with self.assertRaises(IndexError):
            self.editor.undo()

    def test_redo_empty(self):
        with self.assertRaises(IndexError):
            self.editor.redo()

    def test_redo_cleared_on_new_action(self):
        # Regla de oro: si cambias el pasado, se borra tu futuro alternativo
        self.editor.write("A")
        self.editor.undo()
        self.editor.write("B")
        with self.assertRaises(IndexError):
            self.editor.redo() # Ya no deberíamos poder rehacer la "A"

if __name__ == '__main__':
    unittest.main()