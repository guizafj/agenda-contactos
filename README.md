# 📒 Agenda de Contactos

Agenda de Contactos es una aplicación de escritorio desarrollada en Python utilizando Tkinter como interfaz gráfica y SQLite como base de datos. Permite gestionar contactos de manera sencilla y eficiente, ofreciendo funcionalidades completas de CRUD (Crear, Leer, Actualizar, Eliminar).


## Características principales ✨

- 👤 Gestión de Contactos: Añadir, editar y eliminar contactos fácilmente.
- 🔍 Búsqueda Rápida: Buscar contactos por nombre o cualquier otro campo.
- 💾 Persistencia de Datos: Almacenamiento de contactos utilizando SQLite.
- 📄 Exportación e Importación: Exportar e importar contactos en formato CSV.
- 🖥️ Interfaz Intuitiva: Diseño amigable y responsivo con Tkinter/ttk.
- ✅ Validación de Datos: Validación robusta para asegurar la integridad de los datos.
- 🧰 Arquitectura MVC: Estructura del proyecto basada en el patrón Modelo-Vista-Controlador.

## 🛠️ Tecnologías Utilizadas

- Lenguaje de Programación: Python 3.8 o superior
- Interfaz Gráfica: Tkinter / ttk
- Base de Datos: SQLite
- Gestión de Dependencias:`requirements.txt`

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
    └── LICENSE                 # Licencia del proyecto

## ⚙️ Instalación y Ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/guizafj/agenda_contactos_tkinter.git
   cd agenda_contactos_tkinter

2. Crear y Activar un Entorno Virtual (opcional)
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

4. Ejecuta la aplicación:
    ```bash
    python main.py

## Uso 🚀

1. Agregar contacto: Completa el formulario y haz clic en "Guardar"

2. Editar contacto: Selecciona un contacto de la tabla, modifica los datos y haz clic en "Guardar"

3. Eliminar contacto: Selecciona un contacto y haz clic en "Eliminar"

4. Buscar contactos: Usa la barra de búsqueda (por implementar)

5. Importar/exportar: Usa los menús correspondientes (por implementar)

## 📸 Capturas de Pantalla

    Nota: Aquí se incluiran imágenes o gifs que muestren la interfaz de usuario, como la lista de contactos, el formulario de edición, etc.


## Roadmap y mejoras futuras 🔮

* Añadir autenticación de usuarios

* Añadir categorías/etiquetas para contactos

* Soporte para imágenes de perfil

* Exportación a PDF y otros formatos

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas colaborar:

    Haz un fork del repositorio.

    Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).

    Realiza tus cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').

    Sube tus cambios a tu fork (git push origin feature/nueva-funcionalidad).

    Abre un Pull Request describiendo tus cambios.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## 📬 Contacto

Para consultas o sugerencias:

    Autor: guizafj

    Correo: contacto@dguiza.dev