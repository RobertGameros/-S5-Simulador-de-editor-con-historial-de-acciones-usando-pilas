# -S5 Simulador de editor con historial de acciones usando pilas
Tarea Semana 5

# 📝 Simulador de Editor de Texto (LIFO Stack)

**Desarrollado por:** Robert Geovanni Barrios Gameros  
**Carné:** 2890-24-6773  
**Correo:** barriosgamerosrobert@gmail.com  

---

## 📌 Descripción del Proyecto
Este proyecto es un simulador de editor de texto desarrollado en **Python 3**. Implementa un sistema de historial de acciones (Deshacer/Rehacer) utilizando una estructura de datos de **Pila (Stack)** propia basada en el principio **LIFO** (Last In, First Out). 

El proyecto fue diseñado utilizando el patrón de "Comandos", guardando las acciones inversas en lugar del texto completo, lo cual optimiza el uso de memoria. Además, respeta estrictamente la separación de responsabilidades entre la lógica del negocio y la interfaz gráfica.

## 🏗️ Estructura del Proyecto
El código está dividido en 4 módulos para garantizar una arquitectura limpia y modular:

* **`stack.py`**: Implementación de la clase `Stack` nativa (sin librerías externas). Encapsula el comportamiento LIFO (`push`, `pop`, `peek`, `is_empty`, `size`).
* **`editor.py`**: Contiene la clase `TextEditor` con la lógica pura del editor (escribir, borrar, deshacer, rehacer y registrar el historial). Totalmente independiente de la UI.
* **`ui.py`**: Interfaz gráfica construida con `Tkinter`. Captura los eventos del usuario, maneja los errores mediante ventanas emergentes y actualiza el estado visual.
* **`test_editor.py`**: Batería de pruebas unitarias (`unittest`) que validan la robustez de la lógica y los casos límite.

## ✅ Funcionalidades y Validaciones
El sistema cumple con todos los requisitos obligatorios:
1. **write(text):** Agrega texto y limpia la pila de rehacer. Evita escribir texto vacío.
2. **delete(n):** Elimina *n* caracteres. Si se intenta borrar más caracteres de los que existen, ajusta el borrado al máximo disponible.
3. **undo():** Revierte la última acción. Valida si la pila está vacía y lanza excepciones controladas.
4. **redo():** Reaplica una acción deshecha.
5. **show() & history():** Muestra el contenido en tiempo real y una bitácora detallada de las acciones.

## 🚀 Instrucciones de Ejecución

### Requisitos previos
* Python 3.12 o superior.
* No requiere la instalación de librerías externas (solo utiliza módulos de la biblioteca estándar de Python como `tkinter` y `unittest`).

### 1. Ejecutar la Interfaz Gráfica (Aplicación Principal)
Para abrir el editor de texto y probar sus funcionalidades visualmente, abre una terminal en el directorio del proyecto y ejecuta:
```bash
python ui.py

##2. Ejecutar las Pruebas Unitarias (Tests)
Para comprobar la integridad de la estructura de datos y las validaciones de la lógica (9 pruebas en total), ejecuta:

Bash
python test_editor.py
