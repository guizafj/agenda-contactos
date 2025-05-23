"""
Módulo principal de la Agenda de Contactos.

Este archivo es el punto de entrada de la aplicación.
Inicializa e inicia la interfaz gráfica de usuario (GUI) de la agenda,
utilizando la clase AgendaApp definida en el módulo src.gui_agenda.

Autor: Javier Diaz G
Fecha: 19-04-2025
"""

from src.gui_agenda import AgendaApp  # Importamos la clase principal de la GUI

if __name__ == "__main__":
    # Creamos una instancia de la aplicación de agenda
    app = AgendaApp()
    # Iniciamos el bucle principal de la aplicación (mainloop de Tkinter)
    app.mainloop()
