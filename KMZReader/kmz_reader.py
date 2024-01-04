import zipfile
from xml.dom import minidom

class LectorKMZ:

    def __init__(self):
        self.dict_objetos = {}
        self.contador = 1

    def start(self, ruta_kmz):
        contenido_kml = self.extraer_kml_desde_kmz(ruta_kmz)
        doc_kml = minidom.parseString(contenido_kml)
        # Busca e imprime la información de cada Placemark
        self.buscar_informacion_kml(doc_kml)

    def extraer_kml_desde_kmz(self, ruta_kmz):
        # Abre el archivo KMZ y extrae el archivo KML
        with zipfile.ZipFile(ruta_kmz, 'r') as archivo_kmz:
            # Busca el archivo KML dentro del KMZ
            archivos_en_kmz = archivo_kmz.namelist()
            archivo_kml = [archivo for archivo in archivos_en_kmz if archivo.lower().endswith('.kml')]

            if not archivo_kml:
                print("No se encontró ningún archivo KML en el KMZ.")
                return None

            # Lee el contenido del archivo KML
            contenido_kml = archivo_kmz.read(archivo_kml[0])

            return contenido_kml.decode('utf-8')

    def obtener_coordenadas_placemark(self, placemark):
        coordenadas = []

        # Extraer las coordenadas del Placemark si están presentes
        coords = placemark.getElementsByTagName('coordinates')
        if coords:
            coordenada_texto = coords[0].firstChild.nodeValue
            # Dividir las coordenadas en líneas y luego en puntos
            lineas = coordenada_texto.strip().split('\n')
            for linea in lineas:
                puntos = [list(map(float, punto.split(','))) for punto in linea.strip().split()]
                coordenadas.append(puntos)

        return coordenadas

    def obtener_estilo_placemark(self, placemark):
        estilo = {}

        # Buscar el subelemento Style
        styles = placemark.getElementsByTagName('styleUrl')
        if styles:
            estilo = styles[0].firstChild.nodeValue
        return estilo
        


    def buscar_informacion_kml(self, doc_kml):
        # Obtén la lista de elementos "Placemark" en el documento KML
        placemarks = doc_kml.getElementsByTagName('Placemark')

        for placemark in placemarks:
            # Extrae el nombre del Placemark si está presente
            nombres = placemark.getElementsByTagName('name')
            if nombres:
                nombre = nombres[0].firstChild.nodeValue
            else:
                nombre = f"Sin nombre_{self.contador}"
                self.contador += 1

            # Extrae la descripción del Placemark si está presente
            descripciones = placemark.getElementsByTagName('description')
            if descripciones:
                descripcion = descripciones[0].firstChild.nodeValue
            else:
                descripcion = "Sin descripción"

            # Extraer las coordenadas del Placemark
            coordenadas = self.obtener_coordenadas_placemark(placemark)
            # Obtener información del icono
            estilo = self.obtener_estilo_placemark(placemark)

            # Almacena la información del Placemark en el diccionario solo si no es una carpeta sin nombre
            self.dict_objetos[self.contador] = {
                "Nombre": nombre,
                "Descripción": descripcion,
                "Coordenadas": coordenadas[0],
                "Estilo": estilo
            }
            # Incrementa el contador solo si se almacena en el diccionario
            self.contador += 1