

class MigrarInfo:
    
    def __init__(self) -> None:
        self.cID = '122'
        
    def crear_objeto(self, id, oType, vals, vectores):
        nID = self.asignar_nid(oType)
        unixtime = ''
        self.cargar_o(id, nID, unixtime)
        self.cargar_ocfg(id ,oType, nID, unixtime)
        self.cargar_val_y_sidx(vals,id, nID, unixtime)
        self.cargar_v_y_geoidx(vectores,id, nID, unixtime)

    def cargar_o(self,id,net_id, unixtime):
        self.ffo.write(f'SET {self.cID}.{net_id}.{id} "{unixtime}..1."\n')

    def cargar_ocfg(self, id, oType, net_id, unixtime):
        self.ffocfg.write(f'SADD {self.cID}.{net_id}.{id}:ocfg "{unixtime}..1.:{oType}"\n')
    
    def cargar_val_y_sidx(self, id , vals, nID, unixtime):
        pass

    def cargar_v_y_geoidx(self, vectores,id, nID, unixtime):
        count_v = 0
        for v in vectores:
            lat = v[0]
            lon = v[1]
            self.ffv.write(f'SADD {self.cID}.{nID}.{id}:v "{unixtime}..1.:{lon}|{lat}|{count_v}|0"\n')
            self.ffgeoidx.write(f'SADD {self.cID}.{id}:geoidx "{lat} {lon} {unixtime}..1.:{self.cID}.{nID}.{id}|{count_v}|{len(vectores)}"\n')
            count_v += 1
    
    def asignar_nid(self, oType):
        pass