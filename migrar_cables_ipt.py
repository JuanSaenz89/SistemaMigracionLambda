
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
fo_net = '2'
infra_net = '4'


def obtener_cantidad(hilos):
    hilos = str(hilos)
    if hilos == '4':
        return '4', '0'
    elif hilos == '6':
        return '6','0'
    elif hilos == '8':
        return '8','0'
    elif hilos == '12':
        return '12','0'
    elif hilos == '24':
        return '24x12','1'
    elif hilos == '32':
        return '32','4'
    elif hilos == '36':
        return '36','7'
    elif hilos == '48':
        return '48','2'
    elif hilos == '72':
        return '72','3'
    elif hilos == '96':
        return '96', '4'
    elif hilos == '144':
        return '144', '5'
    elif hilos == '288':
        return '288','6'
    else:
        print(hilos)
    

for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']
    lista = i['Cuadro']
    lista = lista[0]
    cantidad_hilos = lista['num_hilo']
    longitud = lista['longitud']
    try:
        localidad = lista['localidad']
    except KeyError:
        localidad = 'Sin Dato'
    try:
        inicio = lista['fo_inicio']
    except KeyError:
        inicio = 'Sin Dato'

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
                            '@longitud':longitud,
                            '@inicio': inicio,
                            '@estado':'E',
                            '@localidad':localidad.capitalize()

                        },
                        nID=fo_net)
    id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración

