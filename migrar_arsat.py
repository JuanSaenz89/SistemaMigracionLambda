
from KMZReader.kmz_reader import LectorKMZ
from KMZReader.db_migration import MigrarInfo
from openpyxl import Workbook

# Suponiendo que ya tienes el contenido_kml del archivo KML
PROVINCIA = 'CHUBUT'
ruta_kmz = f'C:/Users/user/Desktop/Lambda/migraciones/MIGRACION ARSAT/Chubut/{PROVINCIA}.kmz'
path_excel_tramo = 'C:/Users/user/Desktop/Lambda/migraciones/MIGRACION ARSAT/240104 ATRIBUTOS TRAMOS Y DERIVACIONES KMZ V68.xlsx'
path_excel_sitios = ''
lector = LectorKMZ()
# En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx
migrador = MigrarInfo(company_id='30',
                    variables_sidx=['@oName',
                                    '@acronimo',
                                    '@nombre',
                                    '@kmlId',
                                    '@subtramo',
                                    '@tramo'])
lector.start(ruta_kmz)
id_objeto = 13075223
fo_net = '11'
infra_net = '10'

for i in lector.dict_objetos.values():
    nombre = i['Nombre']
    detalle = i['Descripción']
    estilo = i['Estilo']
    coordenadas = i['Coordenadas']
    val = {}

    if 'msn_' in estilo:
        #Si dice la palabra BOX en el nombre se crea un empalme y una caja
        if 'BOX' in nombre:
            migrador.crear_objeto(id=id_objeto,
                            oType='go/fo/cam',
                            vectores=coordenadas,
                            vals={
                                    "@oName": f'{detalle}',
                                    "@tapas": "4",
                                    "@tipoCam": "1",
                                    "@estado":"E",
                                    "@estadoCam":"0",
                                    "@aCaja": f"{nombre}"
                                },
                            nID= infra_net)
            id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración
            migrador.crear_objeto(  id=id_objeto,
                                    oType='go/fo/em',
                                    vectores=coordenadas,
                                    vals={
                                        "@oName": f'{nombre}',
                                        "@posicion": "1",
                                        "@tipoCaja": "5",
                                        "@tipoEmpalme":"2",
                                        "@estadoEm":"E",
                                        "@ocupacion":"1"
                                        },
                                    nID=fo_net)
            id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración
        #Si no lo dice se crea una caja unicamente
        else:
            migrador.crear_objeto(id=id_objeto,
                                oType='go/fo/cam',
                                vectores=coordenadas,
                                vals={
                                    "@oName":f'{nombre}',
                                    "@tapas":"3",
                                    "@tipoCam":"3",
                                    "@estado":"E",
                                    "@propietarioCam":"1",
                                    "@estadoCam":"0"
                                },
                                nID= infra_net)
            id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración

    elif 'square' in estilo:
        #se crea una caja y un empalme, pero es otro tipo de icono en el kmz
        migrador.crear_objeto(id=id_objeto,
                            oType='go/fo/cam',
                            vectores=coordenadas,
                            vals={
                                    "@oName": f'{detalle}',
                                    "@tapas": "4",
                                    "@tipoCam": "1",
                                    "@estado":"E",
                                    "@estadoCam":"0",
                                    "@aCaja": f"{nombre}"
                                },
                            nID= infra_net)
        id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración
        migrador.crear_objeto(  id=id_objeto,
                                oType='go/fo/em',
                                vectores=coordenadas,
                                vals={
                                    "@oName": f'{nombre}',
                                    "@posicion": "1",
                                    "@tipoCaja": "5",
                                    "@tipoEmpalme":"2",
                                    "@estadoEm":"E",
                                    "@ocupacion":"1"
                                    },
                                nID=fo_net)
        id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración

    elif 'inline' in estilo:
        prov = PROVINCIA
    # Cuando es un cable se crea el cable y el tubo en las mismas coordenadas
        migrador.crear_objeto(id=id_objeto,
                            oType='gc/fo',
                            vectores=coordenadas,
                            vals={
                                '@tramo': f'{nombre}',
                                '@propietarioCable': '1',
                                '@mediciones': 'true',
                                '@prov': f'{prov.capitalize()}',
                                '@capacidad':'48',
                                '@buffers':'2',
                                '@marcaFO':'9',
                                '@propietarioInfra':'1',
                                '@datosFO':'5',
                                '@ductosO':'2',
                                '@tipoRed':'1',
                                '@metodo':'1',
                            },
                            nID=fo_net)
        id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración
        migrador.crear_objeto(id=id_objeto,
                            oType='gc/duc',
                            vectores=coordenadas,
                            vals={
                                '@oName': f'{nombre.upper()}',
                                '@nc1': f'{nombre.upper()}',
                                '@ocupacion1': 'true',
                                '@estado': 'E',
                                '@tendido': '1',
                                '@propietarioTri': '1',
                            },
                            nID= infra_net)
        id_objeto += 1  # Incrementar el ID del objeto para la siguiente iteración