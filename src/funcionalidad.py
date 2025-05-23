"""
Módulo funcionalidad.py

Este módulo define la clase Funcionalidad, que actúa como puente entre la base de datos SQLite
y la interfaz gráfica Tkinter para la gestión de contactos. Permite agregar, buscar, modificar,
eliminar, importar y exportar contactos, así como exportarlos en formato vCard.

Autor: Javier Diaz G
Fecha: 04-19-2025
"""

from src.models import Persona
from src.manejo_base_datos import Coneccion
import csv

class Funcionalidad:
    """
    Clase que gestiona la lógica de negocio para la agenda de contactos.
    Permite interactuar con la base de datos y realizar operaciones CRUD,
    así como importar y exportar contactos en diferentes formatos.
    """

    def __init__(self):
        """
        Inicializa la funcionalidad con una conexión a la base de datos.
        """
        self.__persona = None  # Objeto Persona actual
        self.__coneccion = Coneccion()  # Conexión a la base de datos

    @property
    def persona(self):
        """
        Obtiene el objeto Persona actual.
        :return: Instancia de Persona o None
        """
        return self.__persona

    @persona.setter
    def persona(self, persona):
        """
        Establece el objeto Persona actual.
        :param persona: Instancia de Persona
        :raises ValueError: Si el objeto no es una instancia de Persona
        """
        if not isinstance(persona, Persona):
            raise ValueError("El objeto debe ser una instancia de la clase Persona")
        self.__persona = persona

    def agregar_contacto(self):
        """
        Agrega un nuevo contacto a la base de datos.
        :raises ValueError: Si no hay un contacto definido
        """
        if not self.__persona:
            raise ValueError("No hay contacto para agregar")
        self.__persona.validar()  # Validar los datos del contacto
        self.__coneccion.insertar_persona(self.__persona)
        print(f'Contacto {self.__persona.nombre} {self.__persona.apellido} agregado con éxito')

    def buscar_contacto(self, criterio):
        """
        Busca contactos en la base de datos que coincidan con el criterio.
        :param criterio: Texto a buscar en nombre, apellido o email
        :return: Lista de instancias de Persona que coinciden con el criterio
        """
        consulta = (
            'SELECT * FROM personas WHERE nombre LIKE ? OR apellido LIKE ? OR email LIKE ?'
        )
        parametros = (f'%{criterio}%', f'%{criterio}%', f'%{criterio}%')
        try:
            resultados = self.__coneccion._obtener_datos(consulta, parametros)
            return [Persona.from_db_row(fila) for fila in resultados]
        except Exception as e:
            print(f'Error al buscar contacto: {e}')
            return []

    def eliminar_contacto(self, id_contacto):
        """
        Elimina un contacto de la base de datos por su ID.
        :param id_contacto: ID del contacto a eliminar
        :raises ValueError: Si no se proporciona un ID válido
        """
        if not id_contacto:
            raise ValueError("Debe proporcionar un ID válido para eliminar el contacto")
        self.__coneccion.ejecutar_consulta('DELETE FROM personas WHERE id = ?', (id_contacto,))
        print(f'Contacto con ID {id_contacto} eliminado con éxito')

    def modificar_contacto(self):
        """
        Modifica un contacto existente en la base de datos.
        :raises ValueError: Si no hay un contacto definido
        """
        if not self.__persona:
            raise ValueError("No hay contacto para modificar")
        self.__persona.validar()
        consulta = (
            'UPDATE personas SET nombre = ?, apellido = ?, telefono = ?, email = ? WHERE id = ?'
        )
        parametros = (
            self.__persona.nombre,
            self.__persona.apellido,
            self.__persona.telefono,
            self.__persona.email,
            self.__persona.id
        )
        self.__coneccion.ejecutar_consulta(consulta, parametros)
        print(f'Contacto {self.__persona.nombre} {self.__persona.apellido} modificado con éxito')

    def listar_contactos(self):
        """
        Lista todos los contactos de la base de datos.
        :return: Lista de instancias de Persona
        """
        try:
            return self.__coneccion.obtener_personas()
        except Exception as e:
            print(f'Error al listar contactos: {e}')
            return []

    def importar_contactos_desde_csv(self, ruta_archivo):
        """
        Importa contactos desde un archivo CSV y los agrega a la base de datos.
        :param ruta_archivo: Ruta del archivo CSV a importar
        :raises Exception: Si ocurre un error durante la importación
        """
        try:
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    # Se espera que cada fila tenga: nombre, apellido, telefono, email
                    nombre, apellido, telefono, email = fila
                    contacto = Persona(
                        nombre=nombre,
                        apellido=apellido,
                        telefono=telefono,
                        email=email
                    )
                    self.persona = contacto
                    self.agregar_contacto()
        except Exception as e:
            raise Exception(f'Error al importar el archivo CSV: {str(e)}')

    def exportar_contactos_csv(self, ruta_archivo):
        """
        Exporta todos los contactos de la base de datos a un archivo CSV.
        :param ruta_archivo: Ruta del archivo CSV a exportar
        :raises Exception: Si ocurre un error durante la exportación
        """
        try:
            contactos = self.listar_contactos()
            with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                # Escribir la cabecera del archivo CSV
                escritor.writerow(['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email'])
                for contacto in contactos:
                    escritor.writerow([
                        contacto.id,
                        contacto.nombre,
                        contacto.apellido,
                        contacto.telefono,
                        contacto.email
                    ])
            print('Contactos exportados con éxito')
        except Exception as e:
            raise Exception(f"Error al exportar el archivo CSV: {str(e)}")

    def exportar_vcard(self, ruta_archivo):
        """
        Exporta todos los contactos de la base de datos a un archivo en formato vCard.
        :param ruta_archivo: Ruta del archivo vCard a exportar
        """
        contactos = self.listar_contactos()
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            for contacto in contactos:
                f.write("BEGIN:VCARD\n")
                f.write("VERSION:3.0\n")
                f.write(f'FN:{contacto.nombre} {contacto.apellido}\n')
                f.write(f'TEL:{contacto.telefono}\n')
                f.write(f'EMAIL:{contacto.email}\n')
                f.write("END:VCARD\n")


if __name__ == '__main__':
    # Bloque de pruebas para verificar que los métodos funcionan correctamente

    # Crear instancia de Funcionalidad
    funcionalidad = Funcionalidad()

    # Crear una nueva persona y agregarla a la base de datos
    nueva_persona = Persona('Juan', 'Pérez', '123456789', 'juan.perez@example.com')
    funcionalidad.persona = nueva_persona
    funcionalidad.agregar_contacto()

    # Buscar contacto por nombre
    resultados = funcionalidad.buscar_contacto('Juan')
    for resultado in resultados:
        print(resultado)

    # Listar todos los contactos
    contactos = funcionalidad.listar_contactos()
    for contacto in contactos:
        print(contacto)

    # Exportar contactos a un archivo CSV
    funcionalidad.exportar_contactos_csv('contactos.csv')

    # Importar contactos desde un archivo CSV
    funcionalidad.importar_contactos_desde_csv('contactos.csv')

    # Modificar un contacto existente
    if contactos:
        contacto_a_modificar = contactos[0]
        contacto_a_modificar.nombre = 'Juan Carlos'
        funcionalidad.persona = contacto_a_modificar
        funcionalidad.modificar_contacto()

    # Eliminar un contacto por ID
    if contactos:
        funcionalidad.eliminar_contacto(contactos[0].id)