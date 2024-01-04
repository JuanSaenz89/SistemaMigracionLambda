
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo

# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = 'C:/Users/user/Downloads/24-20240104T144640Z-001/Actualización KMZ v68 - 4-1-24/240104 MIGRACION PAIS KMZ V68.kmz'
lector = LectorKMZ()
migrador = MigrarInfo()
lector.start(ruta_kmz)

id_objeto = 1
for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']
    valores = {}
    if 'line' in estilo or 'stylemap' in estilo:
        capacidad = migrador.obtener_capacidad_cable(nombre)
        valores['@foType'] = f'{capacidad}'
        valores['@oName'] = f'{nombre}'
        if 'troncal' in str(nombre.lower()):
            migrador.crear_objeto(id_objeto,'gc/fo',coordenadas, valores, nID= '1')
            id_objeto += 1
        else:
            migrador.crear_objeto(id_objeto,'gc/fo',coordenadas, valores)
            id_objeto += 1
    elif 'triangle' in estilo:
        valores['@oName'] = f'{nombre}'
        migrador.crear_objeto(id_objeto,'go/fo/nap',coordenadas, valores)
        id_objeto += 1
    elif 'target' in estilo:
        valores['@oName'] = f'{nombre}'
        migrador.crear_objeto(id_objeto,'go/fo/gasa',coordenadas, valores)
        id_objeto += 1
    elif 'pushpin' in estilo:
        valores['@oName'] = f'{nombre}'
        migrador.crear_objeto(id_objeto, 'go/fo/cie',coordenadas, valores)
        id_objeto += 1
migrador.hacer_conexiones(id_objeto)