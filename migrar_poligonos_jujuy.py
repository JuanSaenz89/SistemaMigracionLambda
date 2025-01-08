
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo
import re

# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = '/home/linux/Downloads/TECNOLOGIA.kml'
lector = LectorKMZ()
# En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx
migrador = MigrarInfo(company_id='125',
                    variables_sidx=['@oName',
                                    '@acronimo',
                                    '@nombre',
                                    '@kmlId',
                                    '@tramo'])

lector.start(ruta_kmz)
id_objeto = 330000
fo_net = '2'
infra_net = '4'
poligono_net = '5'


for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']
    patron = r"tecnologia:\s*(.*)"

# Extraer el valor
    coincidencia = re.search(patron, detalle)
    if coincidencia:
        tecnologia_valor = coincidencia.group(1)
        
    migrador.crear_objeto(id=id_objeto,
                        oType='a/zona',
                        vectores=coordenadas,
                        vals={
                            '@oName': f'{nombre}',
                            '@tipoproy':f'{tecnologia_valor}',


                        },
                        nID=poligono_net)
    id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración

    print(nombre)
    print("Tecnología:", tecnologia_valor)
    print(estilo)
