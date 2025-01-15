
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo
import json

# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = 'C:/Users/j2sae/Desktop/Trabajo/CAJAS-PROYECTADAS.kmz'
lector = LectorKMZ()
# En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx
migrador = MigrarInfo(company_id='129',
                    variables_sidx=['@oName',
                                    '@acronimo',
                                    '@nombre',
                                    '@kmlId',
                                    '@tramo'])

lector.start(ruta_kmz)
id_objeto = 300
fo_net = '21'
infra_net = '4'
diccionario_json = {}
company_id='129'

def cargarTipoNap(nombre):

    if nombre in 'BOTELLA':
        return '1N'
    elif '01-' in nombre or '02-' in nombre or 'CTO' in nombre or '05-' in nombre or '-P' in nombre or 'P1' in nombre or 'P2' in nombre or 'P6' in nombre:
        return '2N'
    elif 'EMP' in nombre:
        return 'R'
    else:
        return '1N'

count = 1

for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    print(estilo)
    coordenadas = i['Coordenadas']
    #coordenadas = coordenadas[0]
    tipo = cargarTipoNap(nombre)
    '''diccionario_json[count] = {
        "oid": f'{company_id}.{fo_net}.{id_objeto}',
        "ocfg": 'go/fo/cie',
        "longitud": coordenadas[0][1],
        "latitud": coordenadas[0][0],
        "tipo":tipo,
        "nombre": nombre
        }
    count += 1'''
    migrador.crear_objeto(id=id_objeto,
                        oType='go/fo/cie',
                        vectores=coordenadas,
                        vals={
                            '@oName': nombre,
                            '@oType': tipo,
                        },
                        nID=fo_net)

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