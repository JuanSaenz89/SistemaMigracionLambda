
from KMZReader.db_migration import MigrarInfo
from openpyxl import load_workbook
import re

class MigradorBCM():

    # En el objeto MigrarInfo se asignan las variables del ID de la compania y las variables que seran cargadas tambien en el sidx

    migrador = MigrarInfo(company_id='131',
                    variables_sidx=['@oName',
                                    '@kmlId',
                                    ])
    
    def __init__(self):

        # Aqui van las rutas de los excels de clientes y de Splitters y Naps
        self.ruta_excel = '/home/linux/Downloads/Listado por Origen - Estandarizado - Lujan.xlsx'
        self.ruta_excel_clientes = '/home/linux/Downloads/Red por Cliente - Lujan.xlsx'

        self.objectID = 1 # ID en el que se comienza a crear los objetos
        self.fo_net = input('Ingrese el Id de la capa de FO: ')
        self.infra_net = input('Ingrese el Id de la capa de Infraestructura: ')
        self.clientNetID = input('Ingrese el Id de la capa de Clientes: ')

        self.nameList = []
        self.CierresDict = {}
        self.ClientsDict = {}
    
    def start(self):
        self.migrateCierres(self.ruta_excel)


    def migrateCierres(self, filename):
        wb = load_workbook(filename = filename)
        hoja = wb['Listado por Origen']

        for i in range(5,hoja.max_row + 1):
            id = hoja.cell(row=i, column=1).value
            origen = hoja.cell(row=i, column=2).value
            equipamiento = hoja.cell(row=i, column=6).value
            nombre = hoja.cell(row=i, column=6).value
            latitud = hoja.cell(row=i, column=8).value
            longitud = hoja.cell(row=i, column=9).value
            tipo = hoja.cell(row=i, column=10).value
            padreDirecto = hoja.cell(row=i, column=11).value
            direccion = hoja.cell(row=i, column=16).value

            if not latitud or not longitud:
                continue
            
            coordenadas = [[[longitud , latitud]]]
            
            if tipo == 'FO: Distribución / NAP':
                if '_' in equipamiento:
                    equipamiento = equipamiento.split('_')
                    nombre = equipamiento[1]
                
                vals = {
                    '@oName': nombre,
                    '@oType': '2N',
                    '@ref': direccion
                }
                migrador.crear_objeto(id=objectID,
                                oType='go/fo/cie',
                                vectores=coordenadas,
                                vals=vals,
                                nID=fo_net)
                objectID += 1  # Incrementar el ID del objeto para la siguiente iteración
            elif tipo == 'FO: Sangrado / FDH':

                if '_' in equipamiento:
                    equipamiento = equipamiento.split('_')
                    nombre = equipamiento[1]

                if nombre not in nameList:
                    nameList.append(nombre)

                elif nombre in nameList:
                    print(nombre)
                    continue

                vals = {
                    '@oName': nombre,
                    '@oType': '1N',
                    '@ref': direccion
                }
                migrador.crear_objeto(id=objectID,
                                oType='go/fo/cie',
                                vectores=coordenadas,
                                vals=vals,
                                nID=fo_net)
                objectID += 1  # Incrementar el ID del objeto para la siguiente iteración
        
    wb = load_workbook(filename=ruta_excel_clientes)
    hoja = wb['Red Por Cliente']
    unixtime = "1..1."
    for i in range(5,hoja.max_row + 1):
        numero = hoja.cell(row=i, column=1).value
        nombre = hoja.cell(row=i, column=2).value
        domicilio = hoja.cell(row=i, column=3).value
        latitud = hoja.cell(row=i, column=4).value
        longitud = hoja.cell(row=i, column=5).value
        plan = hoja.cell(row=i, column=6).value
        bloqueo = hoja.cell(row=i, column=7).value
        usuario = hoja.cell(row=i, column=8).value
        serialNumber = hoja.cell(row=i, column=9).value
        ontId = hoja.cell(row=i, column=10).value
        ip = hoja.cell(row=i, column=11).value
        mac = hoja.cell(row=i, column=12).value
        cableModem = hoja.cell(row=i, column=13).value
        ssid = hoja.cell(row=i, column=14).value
        claveSsid = hoja.cell(row=i, column=15).value
        ssid5 = hoja.cell(row=i, column=16).value
        claveSsid5 = hoja.cell(row=i, column=17).value
        padreDirecto = hoja.cell(row=i, column=19).value
        padre = hoja.cell(row=i, column=19).value
        com = hoja.cell(row=i, column=20).value

        if not latitud or not longitud:
            continue
        coordenadas = [[[longitud , latitud]]]

        vals = {
            '@oName': numero,
            '@nombre': nombre,
            '@domicilio': domicilio,
            '@plan': plan,
            '@bloqueo': bloqueo,
            '@usuario': usuario,
            '@serialNumber': serialNumber,
            '@ontId': ontId,
            '@ip': ip,
            '@mac': mac,
            '@cableModem': cableModem,
            '@ssid': ssid,
            '@claveSsid': claveSsid,
            '@ssid5': ssid5,
            '@claveSsid5': claveSsid5,
            '@padreDirecto': padreDirecto,
            '@padre': padre,
            '@com': com,
        }
        # Filtrar las claves con valores no None
        vals_filtrados = {k: v for k, v in vals.items() if v is not None}

        migrador.crear_objeto(id=objectID,
                            oType='go/fo/cli',
                            vectores=coordenadas,
                            vals=vals_filtrados,
                            nID=clientNetID)
        self.objectID += 1  # Incrementar el ID del objeto para la siguiente iteración    
