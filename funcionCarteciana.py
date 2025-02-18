import math

coordenada1 = []
coordenada2 = []

def rotateExe(coordenada, grados):
    x, y = coordenada
    theta = math.radians(grados)
    
    xRotated = x * math.cos(theta) - y * math.sin(theta)
    yRotated = x * math.sin(theta) + y * math.cos(theta)

    return xRotated, yRotated

def findPoint(coordenada1, coordenada2):
    #dados dos coordenadas debo girar el norte unos grados hacia la izquierda y encontrar el punto en el que x e y intersectan
    pass