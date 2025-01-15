from scipy.spatial import cKDTree
import time

class MigrarInfo:
    ffo = open('O.txt','a')
    ffocfg = open('OCFG.txt','a')
    ffval = open('VAL.txt','a')
    ffgeoidx = open('GEOIDX.txt','a')
    ffv = open('V.txt','a')
    ffsidx = open('SIDX.txt','a')
    ffco = open('CO.txt','a')
    
    def __init__(self, company_id, variables_sidx) -> None:
        self.cID = company_id
        self.variables_sidx = variables_sidx
        self.cables_fo_coord = {}
        self.cables_fo = {}
        self.cajas_empalme_coord = {}
        self.cajas_empalme = {}
        
    def crear_objeto(self, id, oType, vectores, vals = '', nID = ''):

        """
        The function `crear_objeto` creates an object with a given ID, type, vectors, and optional values
        and new ID.
        
        :param id: el atributo "id" es el identificador unico de cada objeto.
        :param oType: oType is a parameter that represents the type of the object being created
        :param vectores: The parameter "vectores" is a list of vectors
        :param vals: The parameter "vals" is a string that represents the values associated with the object.
        It is optional and can be left empty if there are no values to be assigned
        :param nID: The parameter `nID` is a string that represents the new ID for the object. If it is not
        provided (i.e., `nID == ''`), then the function will assign a new ID using the `asignar_nid` method
        """

        unixtime = int(time.time())
        id_objeto = f'{self.cID}.{nID}.{id}'
        self.cargar_o(id_objeto, unixtime)
        self.cargar_ocfg(id_objeto ,oType, unixtime)
        self.cargar_val_y_sidx(id_objeto, vals ,unixtime)
        self.cargar_v_y_geoidx(vectores,id_objeto, nID, unixtime, oType)

    def cargar_o(self,id, unixtime):
        self.ffo.write(f'SET {id} "{unixtime}..1."\n')

    def cargar_ocfg(self, id, oType, unixtime):
        self.ffocfg.write(f'SADD {id}:ocfg "{unixtime}..1.:{oType}"\n')
    
    def cargar_val_y_sidx(self, id , vals, unixtime):
        for variable, valor in vals.items():
            valor = self.estandarizar(valor)
            self.ffval.write(f'SADD {id}:val "{unixtime}..1.:{variable}|{valor}|0"\n')
            if variable in self.variables_sidx:
                self.ffsidx.write(f'ZADD {self.cID}.{variable}.sidx 0 "{valor}:{unixtime}..1.:{id}"\n')

    def cargar_v_y_geoidx(self, vectores,id, nID, unixtime, oType):
        count_v = 0
        for coord in vectores:
            for v in coord:
                lat = v[0]
                lon = v[1]
                self.ffv.write(f'SADD {id}:v "{unixtime}..1.:{lon}|{lat}|{count_v}|0"\n')
                self.ffgeoidx.write(f'GEOADD {self.cID}.{nID}:geoidx {lat} {lon} "{unixtime}..1.:{id}|{count_v}|{len(vectores)}"\n')
                count_v += 1
    

    # se asigna el network_id segun el tipo de objeto
    def asignar_nid(self, oType):
            if oType == 'go/fo/cie':
                return '1'
            if oType == 'go/fo/nap':
                return '3'
            if oType == 'go/fo/gasa':
                return '4'
            if oType == 'gc/fo':
                return '3'
        
    def obtener_capacidad_cable(self, nombre):
        if "rojo" in nombre:
            return "12"
        elif "verde" in nombre:
            return "24"
        elif "violeta" in nombre:
            return "12x6"
        elif "celeste" in nombre:
            return "12x4"
        elif "amarillo" in nombre:
            return "24"
        elif "azul" in nombre:
            return "12"
        # "SIN DATOS"

    def estandarizar(self, s):
        if not s or type(s) == float:
            return s
        s = s.replace('"', '')
        s = s.replace("'", "")
        s = s.replace("\t", " ")
        s = s.replace("\n"," ")
        s = s.replace("\r", " ")
        s = s.replace(":", " ")
        s = s.replace("|", " ")
        s = s.replace('Á','A')
        s = s.replace('á','a')
        s = s.replace('É', 'E')
        s = s.replace('é', 'e')
        s = s.replace('Í', 'I')
        s = s.replace('í', 'i')
        s = s.replace('Ó', 'O')
        s = s.replace('ó', 'o')
        s = s.replace('Ú', 'U')
        s = s.replace('ú', 'u')
        s = s.replace('Ñ', 'N')
        s = s.replace('ñ', 'n')
        s = s.replace('°','')
        s = s.strip()
        return s
    
    def hacer_conexiones(self, ultimo_id, nid):
        unixtime = int(time.time())
        tree_cables = cKDTree(self.cables_fo_coord)
        tree_cajas = cKDTree(self.cajas_empalme_coord)
        
        # Crear una lista para almacenar las partes divididas de la línea
        lineas_divididas = []

        # Query ball tree para obtener índices de las coordenadas dentro del radio para cada coordenada del árbol dado
        indexes = tree_cajas.query_ball_tree(tree_cables, 0.0000001)
        for i in range(len(indexes)):
            index = indexes[i]
            caja_id = self.cajas_empalme[i]
            # Ordenar los índices para asegurarse de que estén en orden
            index.sort()

            # Dividir la línea según la posición de las cajas de empalme
            for j in range(len(index) + 1):
                if j == 0:
                    start = 0
                else:
                    start = index[j - 1]

                if j == len(index):
                    end = len(self.cables_fo_coord)
                else:
                    end = index[j]

                # Agregar la parte de la línea a la lista
                parte_linea = self.cables_fo_coord[start:end]
                lineas_divididas.append((caja_id, parte_linea))

            # Ahora, lineas_divididas contiene tuplas (caja_id, parte_linea) con las partes de la línea dividida
            # Puedes procesar esta información según tus necesidades
        for caja_id, parte_linea in lineas_divididas:
        # Lista para almacenar los vectores de la nueva línea
            nuevos_vectores = []

            for pos, coord in enumerate(parte_linea):
                # Generar un nuevo ID único que no se repita con los existentes
                nuevo_id = ultimo_id + 1
                nuevo_cable_id = f'{self.cID}.{nid}.{nuevo_id}'

                # Guardar el nuevo ID en la lista de cables_fo
                self.cables_fo.append(nuevo_cable_id)

                # Guardar el vector en la lista de nuevos vectores
                nuevos_vectores.append(coord)

                # Realizar las conexiones correspondientes
                self.ffco.write(f'SADD {nuevo_cable_id}:co "{unixtime}..1.:0|{caja_id}|0"\n')
                self.ffco.write(f'SADD {caja_id}:co "{unixtime}..1.:0|{nuevo_cable_id}|0"\n')

            # Hacer algo con la lista de nuevos vectores, por ejemplo, imprimirlos
            print(f"Vectores de la nueva línea para la caja {caja_id}: {nuevos_vectores}")