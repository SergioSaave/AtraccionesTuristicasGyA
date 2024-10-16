from flask import Flask, render_template, jsonify
from flask_cors import CORS  # Importa CORS
import cv2
import numpy as np
import requests
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# RMChile en EPSG:3857 meters
bbox_x_min = -7884785.215729073  # min x (left)
bbox_x_max = -7848955.358720397  # max x (right)
bbox_y_min = -3969088.2399931327  # min y (bottom)
bbox_y_max = -3941341.5987256127  # max y (top)

def detect_shapes(image):
    hexagon_centers = []

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Blur the image slightly to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply edge detection
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour shape
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        # Check if the approximated contour has 6 sides (hexagon)
        if len(approx) == 6:
            M = cv2.moments(contour)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                hexagon_centers.append((cX, cY))

    return hexagon_centers

def georeference_hex_in_map(hexagon_centers, image_width, image_height):
    georeferenced_centers = []

    # Map each hexagon center to geographic coordinates in EPSG:3857
    for center in hexagon_centers:
        cX, cY = center
        
        # Normalize the coordinates (0 to 1) in terms of the image dimensions
        norm_x = cX / image_width
        norm_y = cY / image_height
        
        # Map normalized coordinates to the bounding box
        x = bbox_x_min + norm_x * (bbox_x_max - bbox_x_min)  # x coordinate (longitude in meters)
        y = bbox_y_min + (1 - norm_y) * (bbox_y_max - bbox_y_min)  # y coordinate (latitude in meters)
        
        georeferenced_centers.append((x, y))
    
    return georeferenced_centers

def load_image_from_url(url):
    # Download the image from the URL
    response = requests.get(url)
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@app.route('/')
def index():
    # URL de la imagen que deseas cargar
    url = "https://stop.carabineros.cl/geoserver/stop/wms/?service=WMS&request=GetMap&version=1.1.1&layers=stop%3ADelitosMayorConnotacionSocial&styles=&format=image%2Fpng&transparent=true&info_format=application%2Fjson&width=3750&height=2904&srs=EPSG%3A3857&bbox=-7884785.215729073%2C-3969088.2399931327%2C-7848955.358720397%2C-3941341.5987256127"
    
    # Carga la imagen desde la URL
    img = load_image_from_url(url)
    
    # Verifica si la imagen se cargó correctamente
    if img is None:
        return "Error al cargar la imagen desde la URL", 500
    
    # Detecta hexágonos
    hexagon_centers = detect_shapes(img)
    
    # Obtén las dimensiones de la imagen
    image_height, image_width = img.shape[:2]
    
    # Georeferencia los centros de los hexágonos
    georeferenced_centers = georeference_hex_in_map(hexagon_centers, image_width, image_height)
    
    # Pasa los centros georeferenciados a la plantilla
    return render_template('index.html', hexagons=georeferenced_centers)

@app.route('/api/hexagons', methods=['GET'])
def get_hexagon_coordinates():
    # URL de la imagen que deseas cargar
    url = "https://stop.carabineros.cl/geoserver/stop/wms/?service=WMS&request=GetMap&version=1.1.1&layers=stop%3ADelitosMayorConnotacionSocial&styles=&format=image%2Fpng&transparent=true&info_format=application%2Fjson&width=3750&height=2904&srs=EPSG%3A3857&bbox=-7884785.215729073%2C-3969088.2399931327%2C-7848955.358720397%2C-3941341.5987256127"
    
    # Carga la imagen desde la URL
    img = load_image_from_url(url)
    
    # Verifica si la imagen se cargó correctamente
    if img is None:
        return jsonify({"error": "Error al cargar la imagen desde la URL"}), 500
    
    # Detecta hexágonos
    hexagon_centers = detect_shapes(img)
    
    # Obtén las dimensiones de la imagen
    image_height, image_width = img.shape[:2]
    
    # Georeferencia los centros de los hexágonos
    georeferenced_centers = georeference_hex_in_map(hexagon_centers, image_width, image_height)

    # Devuelve las coordenadas en formato JSON
    return jsonify(georeferenced_centers)

if __name__ == '__main__':
    app.run(debug=True)
