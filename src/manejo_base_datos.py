"""
Módulo manejo_base_datos.py

Este módulo define la clase Coneccion, que gestiona la conexión y operaciones
con la base de datos SQLite para la agenda de contactos. Permite crear la base,
insertar, consultar y cerrar la conexión, siguiendo buenas prácticas de manejo
de errores y registro de logs.

Autor: Javier Diaz G
Fecha: 19-04-2025
"""

import sqlite3  # Biblioteca para interactuar con bases de datos SQLite
from dotenv import load_dotenv  # Para cargar variables de entorno desde .env
import os  # Para interactuar con el sistema operativo
import logging  # Para registrar errores en un archivo de log
from src.models import Persona  # Clase Persona para mapear los datos

# Configuración del registro de errores
logging.basicConfig(
    filename='errores.log',  # Archivo donde se guardarán los errores
    level=logging.ERROR,  # Nivel de registro (solo errores)
    format='%(asctime)s - %(message)s'  # Formato del mensaje de error
)

class Coneccion:
    """
    Clase para manejar la conexión y operaciones con la base de datos SQLite.

    Métodos públicos:
        - ejecutar_consulta: Ejecuta consultas SQL parametrizadas.
        - insertar_persona: Inserta una nueva persona en la base de datos.
        - obtener_personas: Obtiene todas las personas de la base de datos.
        - obtener_persona_por_id: Obtiene una persona por su ID.
        - cerrar_conexion: Cierra la conexión a la base de datos.
    """

    def __init__(self):
        """
        Inicializa la conexión a la base de datos SQLite y crea la tabla si no existe.
        """
        load_dotenv()  # Carga las variables de entorno desde un archivo .env
        self.__nombre_base_datos = os.getenv('DATABASE_NAME', 'default.db')  # Nombre de la base de datos
        self.__conexion = None  # Variable para la conexión a la base de datos
        self.__cursor = None  # Variable para el cursor de la base de datos
        self._crear_conexion()  # Crea la conexión al inicializar la clase
        self._crear_tabla_personas()  # Crea la tabla 'personas' si no existe

    def _crear_conexion(self):
        """
        Método privado para crear la conexión a la base de datos.
        Lanza RuntimeError si ocurre un error.
        """
        try:
            self.__conexion = sqlite3.connect(self.__nombre_base_datos)
            self.__cursor = self.__conexion.cursor()
            print(f'Conexión exitosa a la base de datos: {self.__nombre_base_datos}')
        except sqlite3.Error as e:
            logging.exception(f'Error al conectar a la base de datos: {self.__nombre_base_datos}')
            raise RuntimeError(f'Error al conectar a la base de datos: {e}')

    def _crear_tabla_personas(self):
        """
        Método privado para crear la tabla 'personas' si no existe.
        Lanza RuntimeError si ocurre un error.
        """
        sql = '''
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
        '''
        try:
            self.__cursor.execute(sql)
            self.__conexion.commit()
            print('Tabla "personas" creada o ya existe')
        except sqlite3.Error as e:
            logging.exception('Error al crear la tabla personas')
            raise RuntimeError(f'Error al crear la tabla personas: {e}')

    def ejecutar_consulta(self, consulta, parametros=()):
        """
        Ejecuta una consulta SQL parametrizada (INSERT, UPDATE, DELETE).

        :param consulta: Consulta SQL a ejecutar.
        :param parametros: Tupla de parámetros para la consulta.
        :raises RuntimeError: Si ocurre un error en la ejecución.
        """
        if not isinstance(consulta, str) or not isinstance(parametros, tuple):
            raise ValueError('La consulta debe ser una cadena y los parámetros deben ser una tupla')
        try:
            self.__cursor.execute(consulta, parametros)
            self.__conexion.commit()
            print('Consulta ejecutada con éxito')
        except sqlite3.Error as e:
            logging.exception(f'Error al ejecutar la consulta: {consulta}')
            raise RuntimeError(f'Error al ejecutar la consulta: {e}')

    def insertar_persona(self, persona):
        """
        Inserta una nueva persona en la base de datos.

        :param persona: Instancia de Persona a insertar.
        :raises TypeError: Si el objeto no es de tipo Persona.
        :raises ValueError: Si los datos de la persona no son válidos.
        """
        if not isinstance(persona, Persona):
            raise TypeError('El objeto debe ser de tipo Persona')
        persona.validar()
        consulta = '''
            INSERT INTO personas (nombre, apellido, telefono, email)
            VALUES (?, ?, ?, ?)
        '''
        self.ejecutar_consulta(consulta, persona.to_tupla())

    def _obtener_datos(self, consulta, parametros=()):
        """
        Ejecuta una consulta SELECT y devuelve los resultados.

        :param consulta: Consulta SQL SELECT.
        :param parametros: Tupla de parámetros para la consulta.
        :return: Lista de tuplas con los resultados.
        :raises RuntimeError: Si ocurre un error en la consulta.
        """
        try:
            self.__cursor.execute(consulta, parametros)
            return self.__cursor.fetchall()
        except sqlite3.Error as e:
            logging.exception(f'Error al obtener datos: {consulta} con parámetros {parametros}')
            raise RuntimeError(f'Error al obtener datos: {e}')

    def obtener_personas(self):
        """
        Obtiene todas las personas de la base de datos.

        :return: Lista de instancias de Persona.
        """
        consulta = 'SELECT * FROM personas'
        filas = self._obtener_datos(consulta)
        return [Persona.from_db_row(fila) for fila in filas]

    def obtener_persona_por_id(self, id_persona):
        """
        Obtiene una persona por su ID.

        :param id_persona: ID de la persona a buscar.
        :return: Instancia de Persona o None si no existe.
        """
        consulta = 'SELECT * FROM personas WHERE id = ?'
        parametros = (id_persona,)
        fila = self._obtener_datos(consulta, parametros)
        if fila:
            return Persona.from_db_row(fila[0])
        return None

    def cerrar_conexion(self):
        """
        Cierra la conexión y el cursor de la base de datos.
        Lanza RuntimeError si ocurre un error.
        """
        try:
            if self.__cursor:
                self.__cursor.close()
            if self.__conexion:
                self.__conexion.close()
            print('Conexión cerrada correctamente')
        except sqlite3.Error as e:
            logging.exception('Error al cerrar la conexión')
            raise RuntimeError(f'Error al cerrar la conexión: {e}')


if __name__ == '__main__':
    # Bloque de pruebas para verificar que los métodos funcionan correctamente

    # Crear instancia de Coneccion
    conexion = Coneccion()

    # Crear una nueva persona y agregarla a la base de datos
    persona = Persona(nombre='Juan', apellido='Pérez', telefono='123456789', email='juan.perez@example.com')
    conexion.insertar_persona(persona)

    # Obtener todas las personas y mostrarlas
    personas = conexion.obtener_personas()
    for p in personas:
        print(p)

    # Obtener una persona por ID y mostrarla
    if personas:
        persona_id = personas[0].id
        persona_obtenida = conexion.obtener_persona_por_id(persona_id)
        print(f'Persona obtenida por ID: {persona_obtenida}')

    # Cerrar la conexión a la base de datos
    conexion.cerrar_conexion()