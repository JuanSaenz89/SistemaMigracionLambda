
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo
import json

# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = 'C:/Users/j2sae/Desktop/Trabajo/P_CLIENTES.kml'
lector = LectorKMZ()
# En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx
migrador = MigrarInfo(company_id='130',
                    variables_sidx=['@oName',
                                    '@acronimo',
                                    '@nombre',
                                    '@kmlId',
                                    '@tramo'])

lector.start(ruta_kmz)
id_objeto = 5000
fo_net = '21'
infra_net = '24'
clientes_net = '22'
diccionario_json = {}
company_id='130'


for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']

    migrador.crear_objeto(id=id_objeto,
                        oType='go/fo/cli',
                        vectores=coordenadas,
                        vals={
                            '@nombre': nombre,
                        },
                        nID=clientes_net)

    id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración



json_string = json.dumps(diccionario_json, indent= 6)

with open('mi_archivo.json', 'w') as archivo:
    archivo.write(json_string)

print("El diccionario se ha convertido y guardado en 'mi_archivo.json'")


# Ejemplo de objeto para crear Json
#"1": {
#   "oid": "125.1.1",
#    "ocfg": "go/fo/cie",
#    "longitud": -24.25931332,
#    "latitud": -65.20265504,
#    "tipo": "4N"
#  },