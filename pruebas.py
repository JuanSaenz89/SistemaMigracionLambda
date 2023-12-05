from KMZReader.kmz_reader import LectorKMZ

count = 0
# Suponiendo que ya tienes el contenido_kml del archivo KML
ruta_kmz = 'C:/Users/user/Downloads/KILOMBO.kmz'

# Crear una instancia de LectorKMZ y ejecutar el método start
lector = LectorKMZ()
lector.start(ruta_kmz)
listaSinDuplicados = set(lector.lista_iconos)
listaSinDuplicados = list(listaSinDuplicados)
for i in listaSinDuplicados:
    print(i)
