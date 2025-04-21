# Agenda de Contactos 📖✏️

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-%230D8ABC)

Aplicación de escritorio para gestión de contactos desarrollada en Python con interfaz gráfica (Tkinter) y base de datos SQLite.


## Características principales ✨

- 🏗️ Arquitectura MVC implícita bien estructurada
- 🗃️ Persistencia de datos con SQLite
- 🖥️ Interfaz gráfica con Tkinter/ttk
- ✅ Validación robusta de datos
- 📊 Operaciones CRUD completas
- 📤📥 Importación/exportación CSV
- 🪵 Sistema de logging de errores

## Requisitos del sistema 💻

- Python 3.8 o superior
- Librerías listadas en `requirements.txt`

## Instalación ⚙️

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/agenda-contactos.git
   cd agenda-contactos

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

3. Ejecuta la aplicación:
    ```bash
    python main.py

## Uso 🚀

1. Agregar contacto: Completa el formulario y haz clic en "Guardar"

2. Editar contacto: Selecciona un contacto de la tabla, modifica los datos y haz clic en "Guardar"

3. Eliminar contacto: Selecciona un contacto y haz clic en "Eliminar"

4. Buscar contactos: Usa la barra de búsqueda (por implementar)

5. Importar/exportar: Usa los menús correspondientes (por implementar)

## Estructura del proyecto 🗂️

/agenda-contactos
│
├── /src
│   ├── gui_agenda.py       # Interfaz gráfica principal
│   ├── manejo_base_datos.py # Clase para manejo de la base de datos
│   ├── funcionalidad.py     # Lógica de negocio
│   ├── models.py           # Modelo de datos (Persona)
│   └── __init__.py         # Para tratar el directorio como paquete
│
├── main.py                 # Punto de entrada de la aplicación
├── .env                    # Configuración de entorno (opcional)
├── requirements.txt        # Dependencias
├── README.md               # Documentación
└── /docs                   # Documentación adicional (opcional)

## Roadmap y mejoras futuras 🔮

* Añadir autenticación de usuarios

* Implementar búsqueda en tiempo real

* Añadir categorías/etiquetas para contactos

* Soporte para imágenes de perfil

* Exportación a PDF y otros formatos

## Contribución 🤝

Las contribuciones son bienvenidas. Por favor abre un issue para discutir los cambios propuestos.

Desarrollado con ❤️ por Francisco J Diaz G