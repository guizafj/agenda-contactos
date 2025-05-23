"""
Módulo gui_agenda.py

Este módulo implementa la interfaz gráfica de usuario (GUI) para la agenda de contactos,
utilizando Tkinter. Permite agregar, buscar, modificar, eliminar, importar y exportar contactos,
así como exportarlos en formato vCard, ahora con una vista de contactos tipo "canvas".

Autor: Javier Diaz G
Fecha: 19-04-2025 (Modificado para vista Canvas el 23-05-2025)
"""

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from tkinter import filedialog, PhotoImage
import os
import csv

from src.funcionalidad import Funcionalidad
from src.models import Persona

class AgendaApp(tk.Tk):
    """
    Clase principal de la aplicación de Agenda de Contactos.
    Maneja la interfaz gráfica y la interacción con la base de datos.
    """

    def __init__(self):
        """
        Inicializa la ventana principal y todos los componentes de la interfaz.
        """
        super().__init__()
        self.id_contacto = None  # ID del contacto seleccionado
        self.funcionalidad = Funcionalidad()  # Lógica de negocio y acceso a la base de datos

        # Configuración inicial de la ventana y widgets
        self.configurar_ventana()
        self.configurar_estilos()
        self.configurar_grid()
        self.mostrar_encabezado()
        self.mostrar_formulario()
        self._setup_contact_canvas() # Cambiado de cargar_canvas a _setup_contact_canvas
        self.mostrar_barra_busqueda()
        self.mostrar_botones()
        self.mostrar_botones_import_export()

    def configurar_ventana(self):
        """
        Configura las propiedades principales de la ventana.
        """
        self.title("Agenda de Contactos")
        self.geometry("1000x600")
        self.configure(background='#1d2d44')
        self.resizable(True, True)  # Permitir redimensionar en ambas direcciones

    def configurar_estilos(self):
        """
        Configura los estilos visuales de los widgets usando ttk.Style.
        """
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam')

        # Estilos generales
        self.estilos.configure('.', font=('Segoe UI', 11))
        self.estilos.configure('TFrame', background='#1d2d44')
        self.estilos.configure('TLabel', background='#1d2d44', foreground='white', font=('Segoe UI', 11, 'bold'))
        self.estilos.configure('TEntry', foreground='#333', fieldbackground='f0f0f0', padding=5, relief='flat')
        self.estilos.map('TEntry', fieldbackground=[('focus', '#e0f7fa')])
        self.estilos.configure('TButton', background='#0077b6', foreground='white', padding=6, relief='flat')
        self.estilos.map('TButton', background=[('active', '#00b4d8'), ('pressed', '#023e8a')], foreground=[('disabled', '#ccc')])

        # Estilos para Canvas (nuevo)
        self.estilos.configure('Canvas', background='#1d2d44', highlightthickness=0)
        
        # Estilos para el scrollbar (si se usa con Canvas)
        self.estilos.configure('Vertical.TScrollbar', background='#0077b6', troughcolor='#1d2d44', bordercolor='#0077b6', arrowcolor='white')
        self.estilos.map('Vertical.TScrollbar', background=[('active', '#00b4d8')])


    def configurar_grid(self):
        """
        Configura el diseño de la cuadrícula principal de la ventana.
        """
        # Configurar el peso de las columnas
        self.columnconfigure(0, weight=1)  # Panel izquierdo (Canvas)
        self.columnconfigure(1, weight=1)  # Panel derecho (Formulario)

        # Configurar el peso de las filas
        self.rowconfigure(0, weight=0)  # Encabezado
        self.rowconfigure(1, weight=0)  # Barra de búsqueda
        self.rowconfigure(2, weight=1)  # Contenido principal (panel izquierdo y derecho)
        self.rowconfigure(3, weight=0)  # Botones de acción
        self.rowconfigure(4, weight=0)  # Botones de import/export

    def mostrar_encabezado(self):
        """
        Muestra el encabezado principal de la aplicación.
        """
        encabezado = ttk.Label(self, text="Agenda de Contactos", style='TLabel', font=('Arial', 20, 'bold'))
        encabezado.grid(row=0, column=0, columnspan=2, pady=10)

    def mostrar_barra_busqueda(self):
        """
        Muestra una barra de búsqueda para filtrar contactos.
        """
        self.frame_busqueda = ttk.Frame(self)
        self.frame_busqueda.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')
        self.frame_busqueda.columnconfigure(1, weight=1)

        # Icono de búsqueda
        lupa = ttk.Label(self.frame_busqueda, text='🕵️', background='#ffffff', font=('Arial', 12))
        lupa.grid(row=0, column=0, padx=(5, 0)) # Cambiado a columna 0 para que la lupa esté a la izquierda

        self.entry_busqueda = ttk.Entry(self.frame_busqueda, style='TEntry', font=('Arial', 11), foreground='grey')
        self.entry_busqueda.insert(0, 'Buscar contacto...')
        self.entry_busqueda.grid(row=0, column=1, padx=5, sticky='ew') # Cambiado a columna 1

        # Eventos para simular el placeholder
        self.entry_busqueda.bind('<FocusIn>', self._clear_placeholder)
        self.entry_busqueda.bind('<FocusOut>', self._add_placeholder)
        self.entry_busqueda.bind('<KeyRelease>', self.filtrar_contactos)

    def _clear_placeholder(self, event):
        """
        Limpia el placeholder de la barra de búsqueda al enfocar.
        """
        if self.entry_busqueda.get() == 'Buscar contacto...':
            self.entry_busqueda.delete(0, 'end')
            self.entry_busqueda.configure(foreground='black')

    def _add_placeholder(self, event):
        """
        Restaura el placeholder si la barra de búsqueda está vacía.
        """
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, 'Buscar contacto...')
            self.entry_busqueda.configure(foreground='grey')
        # No es necesario configurar la fuente aquí, ya está en el estilo TEntry
        # self.entry_busqueda.configure('Arial', 11) 

    def filtrar_contactos(self, event):
        """
        Filtra los contactos según el texto ingresado en la barra de búsqueda y  redibuja en el canvas.
        """
        texto = self.entry_busqueda.get().lower()
        
        # Limpiar el canvas antes de dibujar los contactos filtrados
        self.canvas_contactos.delete("all")

        contactos_filtrados = []
        all_contactos = self.funcionalidad.listar_contactos()
        for contacto in all_contactos:
            if (texto in contacto.nombre.lower() or
                texto in contacto.apellido.lower() or
                texto in contacto.telefono.lower() or
                texto in contacto.email.lower() or
                texto == 'buscar contacto...'): # Si el placeholder está activo, mostrar todos
                contactos_filtrados.append(contacto)
        
        self._draw_all_contacts_on_canvas(contactos_filtrados)


    def mostrar_formulario(self):
        """
        Crea el panel derecho con el formulario para agregar/editar contactos.
        """
        self.panel_derecho = ttk.Frame(self, style='TFrame')
        self.panel_derecho.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

        campos = [("Nombre:", "nombre_e"), ("Apellido:", "apellido_e"),
                  ("Teléfono:", "telefono_e"), ("Email:", "email_e")]

        for i, (label_text, entry_attr) in enumerate(campos):
            label = ttk.Label(self.panel_derecho, text=label_text, style='TLabel')
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(self.panel_derecho, style='TEntry')
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            setattr(self, entry_attr, entry)

        # Configurar el diseño del panel derecho
        self.panel_derecho.columnconfigure(1, weight=1)
        # No es necesario rowconfigure para la última fila si no hay más widgets debajo
        # self.panel_derecho.rowconfigure(len(campos), weight=1)

    def _setup_contact_canvas(self):
        """
        Crea el panel izquierdo con el canvas para mostrar los contactos.
        """
        self.panel_izquierdo = ttk.Frame(self, style='TFrame')
        self.panel_izquierdo.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.canvas_contactos = tk.Canvas(self.panel_izquierdo, bg='#1d2d44', highlightthickness=0)
        self.canvas_contactos.grid(row=0, column=0, sticky='nsew')

        # Configurar scrollbar vertical para el canvas
        self.canvas_scrollbar = ttk.Scrollbar(self.panel_izquierdo, orient='vertical', command=self.canvas_contactos.yview, style='Vertical.TScrollbar')
        self.canvas_scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas_contactos.configure(yscrollcommand=self.canvas_scrollbar.set)

        # Configurar el diseño del panel izquierdo
        self.panel_izquierdo.columnconfigure(0, weight=1)
        self.panel_izquierdo.rowconfigure(0, weight=1)

        # Bind click event to canvas for selection
        self.canvas_contactos.bind('<Button-1>', self._on_canvas_click)

        # Cargar los datos en el canvas
        self.recargar_datos()

    def _draw_contact_on_canvas(self, canvas, contact, y_offset, card_width, card_height):
        """
        Dibuja un único contacto como una "tarjeta" en el canvas, centrado horizontalmente.
        """
        padding_y = 5
        text_x_offset = 15  # Desplazamiento del texto dentro de la tarjeta

        # Obtener el ancho del canvas
        canvas_width = canvas.winfo_width()
        if canvas_width <= 0:  # Si el canvas aún no está inicializado, usar un valor predeterminado
            canvas_width = 400

        # Calcular el desplazamiento horizontal para centrar la tarjeta
        x_offset = (canvas_width - card_width) // 2

        # Coordenadas de la tarjeta
        x1 = x_offset
        y1 = y_offset + padding_y
        x2 = x1 + card_width
        y2 = y1 + card_height

        # Dibujar el rectángulo de la tarjeta
        card_id = canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='#3d5a80', outline='#0077b6', width=2,
            tags=(f"contact_{contact.id}", "contact_card")
        )

        # Dibujar el nombre
        canvas.create_text(
            x1 + text_x_offset, y1 + 15,
            text=f"{contact.nombre} {contact.apellido}",
            anchor='w', fill='white', font=('Segoe UI', 12, 'bold'),
            tags=(f"contact_{contact.id}", "contact_name")
        )

        # Dibujar el teléfono
        canvas.create_text(
            x1 + text_x_offset, y1 + 35,
            text=f"Teléfono: {contact.telefono}",
            anchor='w', fill='white', font=('Segoe UI', 10),
            tags=(f"contact_{contact.id}", "contact_phone")
        )

        # Dibujar el email
        canvas.create_text(
            x1 + text_x_offset, y1 + 55,
            text=f"Email: {contact.email}",
            anchor='w', fill='white', font=('Segoe UI', 10),
            tags=(f"contact_{contact.id}", "contact_email")
        )

        # Asociar eventos de clic con la tarjeta
        canvas.tag_bind(f"contact_{contact.id}", '<Button-1>', self._on_canvas_click)


    def _draw_all_contacts_on_canvas(self, contacts_to_draw):
        """
        Dibuja todos los contactos proporcionados en el canvas.
        """
        self.canvas_contactos.delete("all") # Limpiar el canvas antes de redibujar

        card_height = 70
        card_width = self.canvas_contactos.winfo_width() - 40 # Ancho del canvas menos padding
        if card_width <= 0: # Asegurarse de que el ancho sea positivo antes de dibujar
            card_width = 400 # Valor por defecto si la ventana no está lista

        y_offset = 0
        for contact in contacts_to_draw:
            self._draw_contact_on_canvas(self.canvas_contactos, contact, y_offset, card_width, card_height)
            y_offset += card_height + 10 # Espacio entre tarjetas

        # Actualizar el scrollregion del canvas
        self.canvas_contactos.config(scrollregion=self.canvas_contactos.bbox("all"))

    def recargar_datos(self):
        """
        Limpia y redibuja los contactos en el canvas.
        """
        all_contactos = self.funcionalidad.listar_contactos()
        self._draw_all_contacts_on_canvas(all_contactos)
        # No es necesario bindear <<TreeviewSelect>> aquí, ya se bindea el click del canvas

    def _on_canvas_click(self, event):
        """
        Maneja el evento de clic en el canvas para seleccionar un contacto.
        """
        item_id = self.canvas_contactos.find_closest(event.x, event.y)[0]
        tags = self.canvas_contactos.gettags(item_id)
        
        contact_id = None
        for tag in tags:
            if tag.startswith("contact_"):
                try:
                    contact_id = int(tag.split("_")[1])
                    break
                except ValueError:
                    pass # Ignorar tags que no son IDs de contacto válidos
        
        if contact_id is not None:
            self._select_contact_canvas(contact_id)
            # Resaltar la tarjeta seleccionada (opcional)
            # Primero, deseleccionar cualquier tarjeta previamente seleccionada
            self.canvas_contactos.dtag("selected_card", "selected_card")
            # Luego, seleccionar la nueva tarjeta
            self.canvas_contactos.addtag("selected_card", "contact_card", f"contact_{contact_id}")
            self.canvas_contactos.itemconfig("selected_card", outline='yellow', width=3)
        else:
            # Si se hizo clic en un área sin contacto, limpiar el formulario
            self.limpiar_formulario()


    def _select_contact_canvas(self, contact_id):
        """
        Carga los detalles del contacto seleccionado (por ID) en el formulario.
        """
        contactos = self.funcionalidad.listar_contactos()
        selected_contact = next((c for c in contactos if c.id == contact_id), None)

        if selected_contact:
            self.nombre_e.delete(0, tk.END)
            self.nombre_e.insert(0, selected_contact.nombre)
            self.apellido_e.delete(0, tk.END)
            self.apellido_e.insert(0, selected_contact.apellido)
            self.telefono_e.delete(0, tk.END)
            self.telefono_e.insert(0, selected_contact.telefono)
            self.email_e.delete(0, tk.END)
            self.email_e.insert(0, selected_contact.email)
            self.id_contacto = selected_contact.id
        else:
            self.limpiar_formulario() # Si por alguna razón no se encuentra, limpiar

    def validar_contacto(self):
        """
        Valida los datos del formulario antes de guardar.
        :return: Instancia de Persona válida o None si hay error.
        """
        try:
            contacto = Persona(
                id=self.id_contacto,
                nombre=self.nombre_e.get(),
                apellido=self.apellido_e.get(),
                telefono=self.telefono_e.get(),
                email=self.email_e.get()
            )
            contacto.validar()
            return contacto
        except ValueError as e:
            showerror(title='Error de validación', message=str(e))
            return None

    def guardar_contacto(self):
        """
        Guarda o actualiza un contacto en la base de datos.
        """
        contacto = self.validar_contacto()
        if contacto:
            if self.id_contacto is None:
                self.funcionalidad.persona = contacto
                self.funcionalidad.agregar_contacto()
                showinfo(title='Éxito', message='Contacto guardado correctamente.')
            else:
                self.funcionalidad.persona = contacto
                self.funcionalidad.modificar_contacto()
                showinfo(title='Éxito', message='Contacto actualizado correctamente.')
            self.recargar_datos()
            self.limpiar_formulario() # Limpiar después de guardar/actualizar

    def eliminar_contacto(self):
        """
        Elimina el contacto seleccionado de la base de datos.
        """
        if self.id_contacto is None:
            showerror(title='Atención', message='Seleccione un contacto para eliminar.')
        else:
            self.funcionalidad.eliminar_contacto(self.id_contacto)
            showinfo(title='Éxito', message='Contacto eliminado correctamente.')
            self.recargar_datos()
            self.limpiar_formulario() # Limpiar después de eliminar

    def limpiar_formulario(self):
        """
        Limpia los campos del formulario y reinicia el ID seleccionado.
        """
        if hasattr(self, 'nombre_e'):
            self.nombre_e.delete(0, tk.END)
            self.apellido_e.delete(0, tk.END)
            self.telefono_e.delete(0, tk.END)
            self.email_e.delete(0, tk.END)
            self.id_contacto = None
            # Deseleccionar cualquier tarjeta resaltada en el canvas
            self.canvas_contactos.dtag("selected_card", "selected_card")
        else:
            print("El formulario no ha sido inicializado correctamente.")

    def mostrar_botones(self):
        """
        Muestra los botones de acción (Guardar, Eliminar, Limpiar).
        """
        self.frame_botones = ttk.Frame(self)
        self.frame_botones.grid(row=3, column=0, columnspan=2, pady=10)

        botones = [
            ("Guardar", self.guardar_contacto),
            ("Eliminar", self.eliminar_contacto),
            ("Limpiar", self.limpiar_formulario)
        ]

        for i, (text, command) in enumerate(botones):
            boton = ttk.Button(self.frame_botones, text=text, command=command)
            boton.grid(row=0, column=i, pady=5, padx=20)

    def mostrar_botones_import_export(self):
        """
        Muestra los botones para importar y exportar archivos CSV y vCard.
        """
        self.frame_import_export = ttk.Frame(self)
        self.frame_import_export.grid(row=4, column=0, columnspan=2, pady=10)

        botones_i_e = [
            ('Importar CSV', self.importar_csv),
            ('Exportar CSV', self.exportar_csv),
            ('Exportar vCard', self.exportar_vcard)
        ]

        for i, (text, command) in enumerate(botones_i_e):
            boton = ttk.Button(self.frame_import_export, text=text, command=command)
            boton.grid(row=0, column=i, pady=5, padx=20)

    def importar_csv(self):
        """
        Importa los contactos desde un archivo CSV seleccionado por el usuario.
        """
        ruta_archivo = filedialog.askopenfilename(
            title='Seleccionar archivo CSV',
            filetypes=[('Archivos CSV', '*.csv')]
        )
        if not ruta_archivo:
            return
        try:
            self.funcionalidad.importar_contactos_desde_csv(ruta_archivo)
            showinfo(title='Éxito', message='Contactos importados correctamente.')
            self.recargar_datos()
        except Exception as e:
            showerror(title='Error', message=str(e))

    def exportar_csv(self):
        """
        Exporta los contactos a un archivo CSV seleccionado por el usuario.
        """
        ruta_archivo = filedialog.asksaveasfilename(
            title='Guardar archivo CSV',
            defaultextension='.csv',
            filetypes=[('Archivos CSV', '*.csv')]
        )
        if not ruta_archivo:
            return
        try:
            self.funcionalidad.exportar_contactos_csv(ruta_archivo)
            showinfo(title='Éxito', message='Contactos exportados correctamente.')
        except Exception as e:
            showerror(title='Error', message=str(e))

    def exportar_vcard(self):
        """
        Exporta los contactos a un archivo vCard seleccionado por el usuario.
        """
        ruta_archivo = filedialog.asksaveasfilename(
            title='Guardar archivo vCard',
            defaultextension='.vcard',
            filetypes=[('Archivos vCard', '*.vcard')]
        )
        if not ruta_archivo:
            return
        try:
            self.funcionalidad.exportar_vcard(ruta_archivo)
            showinfo(title='Éxito', message='Contactos exportados correctamente.')
        except Exception as e:
            showerror(title='Error', message=str(e))


