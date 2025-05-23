"""
Módulo models.py

Define la clase Persona, que representa a un contacto en la agenda.
Incluye validaciones, métodos de conversión y utilidades para trabajar
con bases de datos y formularios Tkinter.

Autor: Javier Diaz G
Fecha: 19/04/2025
"""

import re  # Importamos el módulo `re` para trabajar con expresiones regulares (útil para validar emails).


class Persona:
    """
    Clase que representa a una persona en el sistema.
    Contiene atributos como nombre, apellido, teléfono y email,
    y métodos para validación y conversión de datos.
    """

    def __init__(self, nombre="", apellido="", telefono="", email="", id=None):
        """
        Constructor de la clase Persona.
        Inicializa los atributos de la persona con valores predeterminados o los proporcionados.

        :param nombre: Nombre de la persona.
        :param apellido: Apellido de la persona.
        :param telefono: Teléfono de la persona.
        :param email: Correo electrónico de la persona.
        :param id: ID único de la persona (opcional, por defecto None).
        """
        self._id = id  # ID único de la persona (puede ser None si aún no se ha guardado en la base de datos).
        self.__nombre = nombre.strip()  # Eliminamos espacios en blanco al inicio y al final del nombre.
        self.__apellido = apellido.strip()  # Eliminamos espacios en blanco del apellido.
        self.__telefono = telefono.strip()  # Eliminamos espacios en blanco del teléfono.
        self.__email = email.strip()  # Eliminamos espacios en blanco del email.

    @property
    def id(self):
        """
        Propiedad para obtener el ID de la persona.
        :return: ID de la persona.
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Propiedad para establecer el ID de la persona.
        Valida que el ID sea un entero o None.

        :param id: Nuevo ID.
        :raises ValueError: Si el ID no es un entero o None.
        """
        if id is not None and not isinstance(id, int):
            raise ValueError('El id debe ser un entero')  # Lanzamos un error si el ID no es válido.
        self._id = id

    @property
    def nombre(self):
        """
        Propiedad para obtener el nombre de la persona.
        :return: Nombre.
        """
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        """
        Propiedad para establecer el nombre de la persona.
        Valida que el nombre no esté vacío.

        :param nombre: Nuevo nombre.
        :raises ValueError: Si el nombre está vacío.
        """
        if not nombre:  # Si el nombre está vacío, lanzamos un error.
            raise ValueError('El nombre no puede estar vacío')
        self.__nombre = nombre.strip()  # Guardamos el nombre eliminando espacios en blanco.

    @property
    def apellido(self):
        """
        Propiedad para obtener el apellido de la persona.
        :return: Apellido.
        """
        return self.__apellido

    @apellido.setter
    def apellido(self, apellido):
        """
        Propiedad para establecer el apellido de la persona.
        Valida que el apellido no esté vacío.

        :param apellido: Nuevo apellido.
        :raises ValueError: Si el apellido está vacío.
        """
        if not apellido:  # Si el apellido está vacío, lanzamos un error.
            raise ValueError('El apellido no puede estar vacío')
        self.__apellido = apellido.strip()  # Guardamos el apellido eliminando espacios en blanco.

    @property
    def telefono(self):
        """
        Propiedad para obtener el teléfono de la persona.
        :return: Teléfono.
        """
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        """
        Propiedad para establecer el teléfono de la persona.
        Valida que el teléfono sea un número válido.

        :param telefono: Nuevo teléfono.
        :raises ValueError: Si el teléfono no es válido.
        """
        if not telefono or not telefono.isdigit():  # Verificamos que el teléfono no esté vacío y sea numérico.
            raise ValueError('El teléfono debe ser un número válido')
        self.__telefono = telefono.strip()  # Guardamos el teléfono eliminando espacios en blanco.

    @property
    def email(self):
        """
        Propiedad para obtener el email de la persona.
        :return: Email.
        """
        return self.__email

    @email.setter
    def email(self, email):
        """
        Propiedad para establecer el email de la persona.
        Valida que el email tenga un formato válido.

        :param email: Nuevo email.
        :raises ValueError: Si el email no es válido.
        """
        # Usamos una expresión regular para validar el formato del email.
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError('El email debe ser válido')
        self.__email = email.strip()  # Guardamos el email eliminando espacios en blanco.

    def __str__(self):
        """
        Método especial para convertir el objeto Persona a una cadena.
        Útil para depuración o impresión.

        :return: Cadena representando la persona.
        """
        return (f'Persona [id: {self.id}, nombre: {self.nombre}, '
                f'apellido: {self.apellido}, telefono: {self.telefono}, email: {self.email}]')

    def to_tupla(self):
        """
        Convierte el objeto Persona a una tupla.
        Útil para insertar datos en la base de datos.

        :return: Tupla con (nombre, apellido, telefono, email).
        """
        return (self.nombre, self.apellido, self.telefono, self.email)

    def to_dict(self):
        """
        Convierte el objeto Persona a un diccionario.
        Útil para integraciones con Tkinter o para exportar datos.

        :return: Diccionario con los datos de la persona.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email
        }

    def validar(self):
        """
        Valida todos los campos de la persona.
        Lanza un error si algún campo no es válido.

        :raises ValueError: Si algún campo no cumple con los requisitos.
        """
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not self.apellido:
            raise ValueError("El apellido no puede estar vacío")
        if not self.telefono or not self.telefono.isdigit():
            raise ValueError("El teléfono debe ser un número válido")
        if not self.email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email):
            raise ValueError("El email debe ser válido")

    @classmethod
    def from_db_row(cls, row):
        """
        Crea una instancia de Persona a partir de una fila de la base de datos.

        :param row: Tupla con los valores (id, nombre, apellido, telefono, email).
        :return: Instancia de Persona.
        """
        id, nombre, apellido, telefono, email = row  # Desempaquetamos los valores de la fila.
        return cls(nombre=nombre, apellido=apellido, telefono=telefono, email=email, id=id)

    @classmethod
    def from_tkinter(cls, nombre, apellido, telefono, email):
        """
        Crea una instancia de Persona a partir de datos de un formulario de Tkinter.

        :param nombre: Nombre desde el formulario.
        :param apellido: Apellido desde el formulario.
        :param telefono: Teléfono desde el formulario.
        :param email: Email desde el formulario.
        :return: Instancia de Persona.
        """
        return cls(
            nombre=nombre.strip() if nombre else "",
            apellido=apellido.strip() if apellido else "",
            telefono=telefono.strip() if telefono else "",
            email=email.strip() if email else ""
        )

    def to_tkinter(self):
        """
        Convierte el objeto Persona a un formato compatible con Tkinter.
        Devuelve un diccionario con los datos de la persona.

        :return: Diccionario con los datos para Tkinter.
        """
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email
        }