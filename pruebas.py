from shapely.geometry import Point
from shapely.ops import cascaded_union
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo

count = 0
# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = 'C:/Users/user/Downloads/KILOMBO.kmz'

# Crear una instancia de LectorKMZ y ejecutar el método start
lector = LectorKMZ()
lector.start(ruta_kmz)

# Aca se crean listas segun el tipo de objeto, estas deberian de editarse segun que se esta creando, para migrar los objetos po oType
lista_fo = []
lista_nap = []
lista_olt = []
lista_botellas = []

def conectar_objetos(coordenadas, distancia_maxima):
    # Crear geometrías Point a partir de las coordenadas
    puntos = {nombre: Point(coord) for nombre, coord in coordenadas.items()}
    # Crear un buffer alrededor de cada punto
    buffers = {nombre: punto.buffer(distancia_maxima) for nombre, punto in puntos.items()}
    # Unir los buffers para crear una geometría que cubra todas las áreas de búsqueda
    area_busqueda = cascaded_union(list(buffers.values()))
    # Inicializar un diccionario para almacenar las conexiones
    conexiones = {nombre: [] for nombre in coordenadas.keys()}
    # Iterar sobre cada punto y encontrar las conexiones dentro de su buffer
    for nombre_punto, buffer_punto in buffers.items():
        for nombre_otro_punto, buffer_otro_punto in buffers.items():
            if nombre_punto != nombre_otro_punto and buffer_punto.intersects(buffer_otro_punto):
                conexiones[nombre_punto].append(nombre_otro_punto)
    return conexiones
# Ejemplo de uso
coordenadas_ejemplo = {
    'Caja1': (0, 0),
    'Caja2': (2, 0),
    'Cable1': (0, 1),
    'Cable2': (3, 0)
}
distancia_maxima = 1.0  # Distancia máxima para conectar objetos (en metros)
conexiones = conectar_objetos(coordenadas_ejemplo, distancia_maxima)
# Imprimir las conexiones encontradas
for objeto, conexiones_objeto in conexiones.items():
    print(f"{objeto} está conectado con: {conexiones_objeto}")


for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    estilo = i['Estilo']
