
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo

# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = f'/home/linux/Desktop/ARSAT/SistemaMigracionLambda/troncales1.kml'
lector = LectorKMZ()
# En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx
migrador = MigrarInfo(company_id='30',
                    variables_sidx=['@oName',
                                    '@acronimo',
                                    '@nombre',
                                    '@kmlId',
                                    '@tramo'])
lector.start(ruta_kmz)
id_objeto = 528600
fo_net = '31'
infra_net = '30'
patrones_estilo = ['inline', 'msn_ylw-pushpin', '#route', 'geocode']
diccionario_sitios = {}

def obtener_cantidad(hilos):
    pass

for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']
    lista = i['Cuadro']
    cantidad_hilos = lista['num_hilo']
    longitud = lista['longitud']

    cantidad_hilos, buffers = obtener_cantidad(cantidad_hilos)
    tramo = nombre
    migrador.crear_objeto(id=id_objeto,
                        oType='gc/fo',
                        vectores=coordenadas,
                        vals={
                            '@tramo': f'{tramo}',
                            '@mediciones': 'true',
                            '@capacidad':cantidad_hilos,
                            '@buffers':buffers,
                            "@estado":"E",
                        },
                        nID=fo_net)
    id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración

