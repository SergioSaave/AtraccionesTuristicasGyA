import cv2
import numpy as np
import requests
import json

# Parámetros del Bounding Box (en EPSG:3857 metros)
bbox_x_min = -7884785.215729073
bbox_x_max = -7848955.358720397
bbox_y_min = -3969088.2399931327
bbox_y_max = -3941341.5987256127

# Función para detectar hexágonos en la imagen
def detect_shapes(image):
    hexagon_centers = []

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Suavizar la imagen para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detectar bordes
    edged = cv2.Canny(blurred, 50, 150)

    # Encontrar contornos en la imagen con bordes
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Aproximar la forma del contorno
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        # Verificar si el contorno aproximado tiene 6 lados (hexágono)
        if len(approx) == 6:
            M = cv2.moments(contour)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                hexagon_centers.append((cX, cY))

    return hexagon_centers

# Función para georeferenciar las coordenadas de los hexágonos
def georeference_hex_in_map(hexagon_centers, image_width, image_height):
    georeferenced_centers = []

    # Mapear los centros de los hexágonos a coordenadas geográficas en EPSG:3857
    for center in hexagon_centers:
        cX, cY = center
        
        # Normalizar las coordenadas en función de las dimensiones de la imagen
        norm_x = cX / image_width
        norm_y = cY / image_height
        
        # Mapear coordenadas normalizadas al Bounding Box
        x = bbox_x_min + norm_x * (bbox_x_max - bbox_x_min)  # Coordenada x (longitud en metros)
        y = bbox_y_min + (1 - norm_y) * (bbox_y_max - bbox_y_min)  # Coordenada y (latitud en metros)
        
        georeferenced_centers.append((x, y))
    
    return georeferenced_centers

# Función para cargar una imagen desde una URL
def load_image_from_url(url):
    response = requests.get(url)
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

# URL de la imagen (de tu WMS)
url = "https://stop.carabineros.cl/geoserver/stop/wms/?service=WMS&request=GetMap&version=1.1.1&layers=stop%3ADelitosMayorConnotacionSocial&styles=&format=image%2Fpng&transparent=true&info_format=application%2Fjson&width=3750&height=2904&srs=EPSG%3A3857&bbox=-7884785.215729073%2C-3969088.2399931327%2C-7848955.358720397%2C-3941341.5987256127"

# Cargar la imagen desde la URL
img = load_image_from_url(url)

if img is not None:
    # Detectar hexágonos
    hexagon_centers = detect_shapes(img)

    # Obtener las dimensiones de la imagen
    image_height, image_width = img.shape[:2]

    # Georeferenciar los centros de los hexágonos
    georeferenced_centers = georeference_hex_in_map(hexagon_centers, image_width, image_height)

    # Guardar las coordenadas en un archivo JSON
    with open('metadataSTOP.json', 'w') as json_file:
        json.dump(georeferenced_centers, json_file, indent=4)
    
    print("Las coordenadas georeferenciadas de los hexágonos se han guardado en 'hexagon_coordinates.json'.")
else:
    print("Error al cargar la imagen.")
