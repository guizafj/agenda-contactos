from src.funcionalidad import Funcionalidad  # Importamos la clase Funcionalidad para interactuar con la base de datos
from src.models import Persona  # Importamos la clase Persona para representar los contactos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk  # Submódulo de tkinter para widgets avanzados
from tkinter.messagebox import showinfo, showerror  # Para mostrar mensajes emergentes

class AgendaApp(tk.Tk):
    """
    Clase principal de la aplicación de Agenda de Contactos.
    Maneja la interfaz gráfica y la interacción con la base de datos.
    """
    def __init__(self):
        super().__init__()  # Inicializamos la clase base (tk.Tk)
        self.id_contacto = None  # ID del contacto seleccionado (None significa que no hay contacto seleccionado)
        self.funcionalidad = Funcionalidad()  # Instancia de Funcionalidad para interactuar con la base de datos
        self.configurar_ventana()  # Configuramos la ventana principal
        self.configurar_estilos()  # Configuramos los estilos de los widgets
        self.configurar_grid()  # Configuramos el diseño de la cuadrícula
        self.mostrar_encabezado()  # Mostramos el encabezado de la aplicación
        self.mostrar_formulario()  # Creamos y mostramos el formulario para los datos del contacto
        self.cargar_tabla()  # Creamos y cargamos la tabla para mostrar los contactos
        self.mostrar_botones()  # Mostramos los botones de acción

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Agenda de Contactos")  # Título de la ventana
        self.geometry("1000x600")  # Tamaño de la ventana
        self.configure(background='#1d2d44')  # Color de fondo de la ventana

    def configurar_estilos(self):
        """Configura los estilos de los widgets."""
        self.estilos = ttk.Style()  # Creamos un objeto de estilo
        self.estilos.theme_use('clam')  # Usamos el tema 'clam' para los widgets
        self.estilos.configure('TFrame', background='#1d2d44')  # Fondo de los marcos
        self.estilos.configure('TLabel', background='#1d2d44', foreground='white')  # Estilo de las etiquetas
        self.estilos.configure('TEntry', foreground='white', fieldbackground='black')  # Estilo de las entradas de texto
        self.estilos.configure('TButton', background='#005f73', foreground='white')  # Estilo de los botones
        self.estilos.map('TButton', background=[('active', '#0a9396')], foreground=[('active', 'white')])  # Estilo al pasar el mouse

    def configurar_grid(self):
        """Configura el diseño de la cuadrícula."""
        self.columnconfigure(0, weight=1)  # Configuramos la columna 0 para que se ajuste al tamaño disponible
        self.columnconfigure(1, weight=1)  # Configuramos la columna 1 para que se ajuste al tamaño disponible

    def mostrar_encabezado(self):
        """Muestra el encabezado de la aplicación."""
        encabezado = ttk.Label(self, text="Agenda de Contactos", style='TLabel')  # Creamos una etiqueta
        encabezado.grid(row=0, column=0, columnspan=2, pady=10)  # La colocamos en la parte superior de la ventana

    def mostrar_formulario(self):
        """Crea y muestra el formulario para los datos del contacto."""
        self.frame_formulario = ttk.Frame(self, style='TFrame')  # Creamos un marco para el formulario
        self.frame_formulario.grid(row=1, column=0, padx=10, pady=10)  # Lo colocamos en la ventana

        # Lista de campos del formulario (etiqueta y nombre del atributo)
        campos = [("Nombre:", "nombre_e"), ("Apellido:", "apellido_e"), 
                  ("Teléfono:", "telefono_e"), ("Email:", "email_e")]

        # Creamos las etiquetas y entradas de texto para cada campo
        for i, (label_text, entry_attr) in enumerate(campos):
            label = ttk.Label(self.frame_formulario, text=label_text, style='TLabel')  # Etiqueta
            label.grid(row=i, column=0, padx=5, pady=5)  # Posición de la etiqueta
            entry = ttk.Entry(self.frame_formulario, style='TEntry')  # Entrada de texto
            entry.grid(row=i, column=1, padx=5, pady=5)  # Posición de la entrada
            setattr(self, entry_attr, entry)  # Guardamos la entrada como un atributo de la clase

    def cargar_tabla(self):
        """Carga los datos en la tabla."""
        self.frame_tabla = ttk.Frame(self)  # Creamos un marco para la tabla
        self.frame_tabla.grid(row=1, column=1, padx=20)  # Lo colocamos en la ventana

        # Creamos la tabla con columnas para los datos del contacto
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("ID", "Nombre", "Apellido", "Teléfono", "Email"), show="headings")
        self.tabla.heading("ID", text="ID")  # Encabezado de la columna ID
        self.tabla.heading("Nombre", text="Nombre")  # Encabezado de la columna Nombre
        self.tabla.heading("Apellido", text="Apellido")  # Encabezado de la columna Apellido
        self.tabla.heading("Teléfono", text="Teléfono")  # Encabezado de la columna Teléfono
        self.tabla.heading("Email", text="Email")  # Encabezado de la columna Email
        self.tabla.column("ID", width=50, anchor="center")  # Configuración de la columna ID
        self.tabla.column("Nombre", width=150, anchor="center")  # Configuración de la columna Nombre
        self.tabla.column("Apellido", width=150, anchor="center")  # Configuración de la columna Apellido
        self.tabla.column("Teléfono", width=100, anchor="center")  # Configuración de la columna Teléfono
        self.tabla.column("Email", width=200, anchor="center")  # Configuración de la columna Email
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_contacto)  # Vinculamos un evento para seleccionar un contacto
        self.tabla.grid(row=0, column=0)  # Colocamos la tabla en el marco

        # Agregamos un scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)  # Vinculamos el scrollbar a la tabla
        scrollbar.grid(row=0, column=1, sticky='ns')  # Colocamos el scrollbar

        self.recargar_datos()  # Cargamos los datos en la tabla

    def cargar_contacto(self, event):
        """Carga los datos del contacto seleccionado en el formulario."""
        try:
            elemento_seleccionado = self.tabla.selection()[0]  # Obtenemos el elemento seleccionado
            contacto = self.tabla.item(elemento_seleccionado)['values']  # Obtenemos los valores del contacto
            self.id_contacto, nombre, apellido, telefono, email = contacto  # Desempaquetamos los valores
            # Cargamos los valores en el formulario
            self.nombre_e.delete(0, tk.END)
            self.nombre_e.insert(0, nombre)
            self.apellido_e.delete(0, tk.END)
            self.apellido_e.insert(0, apellido)
            self.telefono_e.delete(0, tk.END)
            self.telefono_e.insert(0, telefono)
            self.email_e.delete(0, tk.END)
            self.email_e.insert(0, email)
        except IndexError:
            pass  # Si no hay selección, no hacemos nada

    def validar_contacto(self):
        """Valida los datos del formulario antes de guardar."""
        try:
            # Creamos un objeto Persona con los datos del formulario
            contacto = Persona(
                id=self.id_contacto,
                nombre=self.nombre_e.get(),
                apellido=self.apellido_e.get(),
                telefono=self.telefono_e.get(),
                email=self.email_e.get()
            )
            contacto.validar()  # Validamos los datos usando el método de la clase Persona
            return contacto
        except ValueError as e:
            showerror(title='Error de validación', message=str(e))  # Mostramos un mensaje de error si los datos no son válidos
            return None

    def guardar_contacto(self):
        """Guarda o actualiza un contacto."""
        contacto = self.validar_contacto()  # Validamos los datos del formulario
        if contacto:
            if self.id_contacto is None:  # Si no hay ID, es un nuevo contacto
                self.funcionalidad.persona = contacto
                self.funcionalidad.agregar_contacto()
                showinfo(title='Éxito', message='Contacto guardado correctamente.')
            else:  # Si hay ID, actualizamos el contacto existente
                self.funcionalidad.persona = contacto
                self.funcionalidad.modificar_contacto()
                showinfo(title='Éxito', message='Contacto actualizado correctamente.')
            self.recargar_datos()  # Recargamos los datos en la tabla

    def eliminar_contacto(self):
        """Elimina el contacto seleccionado."""
        if self.id_contacto is None:  # Si no hay contacto seleccionado, mostramos un error
            showerror(title='Atención', message='Seleccione un contacto para eliminar.')
        else:
            self.funcionalidad.eliminar_contacto(self.id_contacto)  # Eliminamos el contacto
            showinfo(title='Éxito', message='Contacto eliminado correctamente.')
            self.recargar_datos()  # Recargamos los datos en la tabla

    def mostrar_botones(self):
        """Muestra los botones de acción."""
        self.frame_botones = ttk.Frame(self)  # Creamos un marco para los botones
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=20)  # Lo colocamos en la ventana

        # Lista de botones (texto y función asociada)
        botones = [
            ("Guardar", self.guardar_contacto),
            ("Eliminar", self.eliminar_contacto),
            ("Limpiar", self.limpiar_formulario)
        ]

        # Creamos los botones y los colocamos en el marco
        for i, (text, command) in enumerate(botones):
            boton = ttk.Button(self.frame_botones, text=text, command=command)
            boton.grid(row=0, column=i, pady=10, padx=30)

    def recargar_datos(self):
        """Recarga los datos de la tabla."""
        for item in self.tabla.get_children():  # Eliminamos todos los elementos de la tabla
            self.tabla.delete(item)
        contactos = self.funcionalidad.listar_contactos()  # Obtenemos los contactos de la base de datos
        for contacto in contactos:  # Agregamos cada contacto a la tabla
            self.tabla.insert('', tk.END, values=(contacto.id, contacto.nombre, contacto.apellido, contacto.telefono, contacto.email))
        self.limpiar_formulario()  # Limpiamos el formulario

    def limpiar_formulario(self):
        """Limpia el formulario."""
        if hasattr(self, 'nombre_e'):  # Verificamos que el formulario esté inicializado
            self.nombre_e.delete(0, tk.END)
            self.apellido_e.delete(0, tk.END)
            self.telefono_e.delete(0, tk.END)
            self.email_e.delete(0, tk.END)
            self.id_contacto = None  # Reiniciamos el ID del contacto seleccionado
        else:
            print("El formulario no ha sido inicializado correctamente.")  # Mensaje de depuración