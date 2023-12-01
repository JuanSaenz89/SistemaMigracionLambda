from KMZReader.kmz_reader import LectorKMZ

ruta_kmz = 'C:/Users/user/Downloads/CS.kmz'
count = 0
# Crear una instancia de LectorKMZ y ejecutar el método start
lector = LectorKMZ()
lector.start(ruta_kmz)

# Acceder al diccionario de objetos con la información recopilada
print("Diccionario de objetos:")
for numero, objeto_info in lector.dict_objetos.items():
    if objeto_info['CarpetaPadre'] in ['CE','CTO']  :
        count += 1
print(count)