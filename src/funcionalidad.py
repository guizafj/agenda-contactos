from src.models import Persona
from src.manejo_base_datos import Coneccion
import csv

class Funcionalidad:
    """
    Clase que actúa como puente entre la base de datos SQLite y la interfaz gráfica Tkinter.
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
        Propiedad para obtener el objeto Persona actual.
        """
        return self.__persona

    @persona.setter
    def persona(self, persona):
        """
        Propiedad para establecer el objeto Persona actual.
        Valida que el objeto sea una instancia de la clase Persona.
        """
        if not isinstance(persona, Persona):
            raise ValueError("El objeto debe ser una instancia de la clase Persona")
        self.__persona = persona

    def agregar_contacto(self):
        """
        Agrega un nuevo contacto a la base de datos.
        """
        if not self.__persona:
            raise ValueError("No hay contacto para agregar")
        self.__persona.validar()  # Validamos los datos del contacto
        self.__coneccion.insertar_persona(self.__persona)  # Usamos el método de manejo_base_datos
        print(f'Contacto {self.__persona.nombre} {self.__persona.apellido} agregado con éxito')

    def buscar_contacto(self, criterio):
        """
        Busca contactos en la base de datos que coincidan con el criterio.
        """
        consulta = '''SELECT * FROM personas WHERE nombre LIKE ? OR apellido LIKE ? OR email LIKE ?'''
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
        """
        if not id_contacto:
            raise ValueError("Debe proporcionar un ID válido para eliminar el contacto")
        self.__coneccion.ejecutar_consulta('DELETE FROM personas WHERE id = ?', (id_contacto,))
        print(f'Contacto con ID {id_contacto} eliminado con éxito')

    def modificar_contacto(self):
        """
        Modifica un contacto existente en la base de datos.
        """
        if not self.__persona:
            raise ValueError("No hay contacto para modificar")
        self.__persona.validar()  # Validamos los datos del contacto
        consulta = '''UPDATE personas SET nombre = ?, apellido = ?, telefono = ?, email = ? WHERE id = ?'''
        parametros = (self.__persona.nombre, self.__persona.apellido, self.__persona.telefono, self.__persona.email, self.__persona.id)
        self.__coneccion.ejecutar_consulta(consulta, parametros)
        print(f'Contacto {self.__persona.nombre} {self.__persona.apellido} modificado con éxito')

    def listar_contactos(self):
        """
        Lista todos los contactos de la base de datos.
        """
        try:
            return self.__coneccion.obtener_personas()  # Usamos el método de manejo_base_datos
        except Exception as e:
            print(f'Error al listar contactos: {e}')
            return []

    def importar_contactos(self, archivo_csv):
        """
        Importa contactos desde un archivo CSV.
        """
        try:
            with open(archivo_csv, 'r') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    if len(fila) != 4:
                        print(f'Error: la fila {fila} no tiene el formato correcto')
                        continue
                    nombre, apellido, telefono, email = fila
                    persona = Persona(nombre=nombre, apellido=apellido, telefono=telefono, email=email)
                    persona.validar()  # Validamos los datos antes de insertarlos
                    self.__coneccion.insertar_persona(persona)
                print('Contactos importados con éxito')
        except FileNotFoundError:
            print('Error: el archivo no existe')
        except Exception as e:
            print(f'Error al importar contactos: {e}')

    def exportar_contactos(self, archivo_csv):
        """
        Exporta todos los contactos a un archivo CSV.
        """
        contactos = self.listar_contactos()
        try:
            with open(archivo_csv, 'w', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email'])  # Cabecera del archivo CSV
                for contacto in contactos:
                    escritor.writerow([contacto.id, contacto.nombre, contacto.apellido, contacto.telefono, contacto.email])
            print('Contactos exportados con éxito')
        except Exception as e:
            print(f'Error al exportar contactos: {e}')


if __name__ == '__main__':
    # Bloque de pruebas para verificar que los métodos funcionan correctamente
    funcionalidad = Funcionalidad()

    # Crear una nueva persona
    nueva_persona = Persona('Juan', 'Pérez', '123456789', 'juan.perez@example.com')
    funcionalidad.persona = nueva_persona
    funcionalidad.agregar_contacto()  # Agregar contacto a la base de datos

    # Buscar contacto
    resultados = funcionalidad.buscar_contacto('Juan')
    for resultado in resultados:
        print(resultado)

    # Listar contactos
    contactos = funcionalidad.listar_contactos()
    for contacto in contactos:
        print(contacto)

    # Exportar contactos a un archivo CSV
    funcionalidad.exportar_contactos('contactos.csv')

    # Importar contactos desde un archivo CSV
    funcionalidad.importar_contactos('contactos.csv')

    # Modificar un contacto
    if contactos:
        contacto_a_modificar = contactos[0]
        contacto_a_modificar.nombre = 'Juan Carlos'
        funcionalidad.persona = contacto_a_modificar
        funcionalidad.modificar_contacto()

    # Eliminar un contacto
    if contactos:
        funcionalidad.eliminar_contacto(contactos[0].id)