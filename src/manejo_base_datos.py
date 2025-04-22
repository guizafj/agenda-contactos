import sqlite3  # Biblioteca para interactuar con bases de datos SQLite
from dotenv import load_dotenv  # Biblioteca para cargar variables de entorno desde un archivo .env
import os  # Biblioteca para interactuar con el sistema operativo
import logging  # Biblioteca para registrar errores en un archivo de log
from src.models import Persona  # Importamos la clase Persona del módulo models.py

# Configuración del registro de errores
logging.basicConfig(
    filename='errores.log',  # Archivo donde se guardarán los errores
    level=logging.ERROR,  # Nivel de registro (solo errores)
    format='%(asctime)s - %(message)s'  # Formato del mensaje de error
)

class Coneccion:
    """
    Clase para manejar la conexión a la base de datos SQLite.
    Proporciona métodos para interactuar con la base de datos.
    """
    def __init__(self):
        """
        Inicializa la conexión a la base de datos SQLite.
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
        """
        try:
            # Conectamos a la base de datos
            self.__conexion = sqlite3.connect(self.__nombre_base_datos)
            self.__cursor = self.__conexion.cursor()  # Creamos un cursor para ejecutar consultas
            print(f'Conexión exitosa a la base de datos: {self.__nombre_base_datos}')
        except sqlite3.Error as e:
            # Registramos el error en el archivo de log y lanzamos una excepción
            logging.exception(f'Error al conectar a la base de datos: {self.__nombre_base_datos}')
            raise RuntimeError(f'Error al conectar a la base de datos: {e}')

    def _crear_tabla_personas(self):
        """
        Método privado para crear la tabla 'personas' si no existe.
        """
        sql = '''
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID autoincremental
                nombre TEXT NOT NULL,  -- Nombre de la persona
                apellido TEXT NOT NULL,  -- Apellido de la persona
                telefono TEXT NOT NULL,  -- Teléfono de la persona
                email TEXT NOT NULL  -- Email de la persona
            )
        '''
        try:
            self.__cursor.execute(sql)  # Ejecutamos la consulta para crear la tabla
            self.__conexion.commit()  # Guardamos los cambios en la base de datos
            print('Tabla "personas" creada o ya existe')
        except sqlite3.Error as e:
            # Registramos el error en el archivo de log y lanzamos una excepción
            logging.exception('Error al crear la tabla personas')
            raise RuntimeError(f'Error al crear la tabla personas: {e}')

    def ejecutar_consulta(self, consulta, parametros=()):
        """
        Método público para ejecutar consultas SQL parametrizadas.
        """
        if not isinstance(consulta, str) or not isinstance(parametros, tuple):
            raise ValueError('La consulta debe ser una cadena y los parámetros deben ser una tupla')
        try:
            self.__cursor.execute(consulta, parametros)  # Ejecutamos la consulta con los parámetros
            self.__conexion.commit()  # Guardamos los cambios en la base de datos
            print('Consulta ejecutada con éxito')
        except sqlite3.Error as e:
            # Registramos el error en el archivo de log y lanzamos una excepción
            logging.exception(f'Error al ejecutar la consulta: {consulta}')
            raise RuntimeError(f'Error al ejecutar la consulta: {e}')

    def insertar_persona(self, persona):
        """
        Método público para insertar una nueva persona en la base de datos.
        """
        if not isinstance(persona, Persona):
            raise TypeError('El objeto debe ser de tipo Persona')  # Validamos que sea una instancia de Persona
        persona.validar()  # Validamos los datos de la persona antes de insertarla
        consulta = '''
            INSERT INTO personas (nombre, apellido, telefono, email)
            VALUES (?, ?, ?, ?)
        '''
        self.ejecutar_consulta(consulta, persona.to_tupla())  # Insertamos la persona en la base de datos

    def _obtener_datos(self, consulta, parametros=()):
        """
        Método privado para ejecutar consultas SELECT y devolver los resultados.
        """
        try:
            self.__cursor.execute(consulta, parametros)  # Ejecutamos la consulta con los parámetros
            return self.__cursor.fetchall()  # Devolvemos todas las filas obtenidas
        except sqlite3.Error as e:
            # Registramos el error en el archivo de log y lanzamos una excepción
            logging.exception(f'Error al obtener datos: {consulta} con parámetros {parametros}')
            raise RuntimeError(f'Error al obtener datos: {e}')

    def obtener_personas(self):
        """
        Método público para obtener todas las personas de la base de datos.
        """
        consulta = 'SELECT * FROM personas'  # Consulta para obtener todas las personas
        filas = self._obtener_datos(consulta)  # Obtenemos las filas de la base de datos
        return [Persona.from_db_row(fila) for fila in filas]  # Convertimos las filas en objetos Persona

    def obtener_persona_por_id(self, id_persona):
        """
        Método público para obtener una persona por su ID.
        """
        consulta = 'SELECT * FROM personas WHERE id = ?'  # Consulta para obtener una persona por ID
        parametros = (id_persona,)  # Parámetros de la consulta
        fila = self._obtener_datos(consulta, parametros)  # Obtenemos la fila de la base de datos
        if fila:
            return Persona.from_db_row(fila[0])  # Convertimos la fila en un objeto Persona
        return None  # Si no se encuentra la persona, devolvemos None

    def cerrar_conexion(self):
        """
        Método público para cerrar la conexión a la base de datos.
        """
        try:
            if self.__cursor:
                self.__cursor.close()  # Cerramos el cursor
            if self.__conexion:
                self.__conexion.close()  # Cerramos la conexión
            print('Conexión cerrada correctamente')
        except sqlite3.Error as e:
            # Registramos el error en el archivo de log y lanzamos una excepción
            logging.exception('Error al cerrar la conexión')
            raise RuntimeError(f'Error al cerrar la conexión: {e}')

if __name__ == '__main__':
    # Bloque de pruebas para verificar que los métodos funcionan correctamente
    conexion = Coneccion()

    # Crear una nueva persona
    persona = Persona(nombre='Juan', apellido='Pérez', telefono='123456789', email='juan.perez@example.com')
    conexion.insertar_persona(persona)  # Insertamos la persona en la base de datos

    # Obtener todas las personas
    personas = conexion.obtener_personas()  # Obtenemos todas las personas de la base de datos
    for p in personas:
        print(p)  # Imprimimos cada persona

    # Obtener una persona por ID
    if personas:
        persona_id = personas[0].id  # Obtenemos el ID de la primera persona
        persona_obtenida = conexion.obtener_persona_por_id(persona_id)  # Obtenemos la persona por ID
        print(f'Persona obtenida por ID: {persona_obtenida}')

    # Cerrar la conexión
    conexion.cerrar_conexion()  # Cerramos la conexión a la base de datos