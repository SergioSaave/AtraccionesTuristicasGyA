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

MIN_LAT = -33.54912050860342  # Límite sur
MIN_LON = -70.79795837402345  # Límite oeste
MAX_LAT = -33.35834837283271  # Límite norte
MAX_LON = -70.52639007568361  # Límite este

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

@app.route('/iglesias', methods=['GET'])
def iglesias_handler():
    # Define la URL base de Overpass API
    base_url = "https://overpass-api.de/api/interpreter"

    # Define las coordenadas del bounding box
    min_lat = -33.54912050860342  # Límite sur
    min_lon = -70.79795837402345  # Límite oeste
    max_lat = -33.35834837283271  # Límite norte
    max_lon = -70.52639007568361  # Límite este

    # Define la consulta con el bounding box y los filtros
    query = f"""
    [out:json][timeout:25];
    nwr["amenity"="place_of_worship"]["religion"="christian"]({min_lat},{min_lon},{max_lat},{max_lon});
    out geom;
    """

    # Haz la solicitud HTTP POST
    response = requests.post(base_url, data={'data': query})

    # Verifica si la respuesta fue exitosa
    if response.status_code != 200:
        return jsonify({"error": "Error en la solicitud a Overpass API"}), response.status_code

    # Retorna la respuesta JSON de Overpass API
    return jsonify(response.json())

@app.route('/monumentos', methods=['GET'])
def monumentos_handler():
    # Define la URL base de Overpass API
    base_url = "https://overpass-api.de/api/interpreter"

    # Define las coordenadas del bounding box
    min_lat = -33.54912050860342  # Límite sur
    min_lon = -70.79795837402345  # Límite oeste
    max_lat = -33.35834837283271  # Límite norte
    max_lon = -70.52639007568361  # Límite este

    # Define la consulta con el bounding box y los filtros
    query = f"""
    [out:json][timeout:25];
    nwr["historic"="monument"]({min_lat},{min_lon},{max_lat},{max_lon});
    out geom;
    """

    # Haz la solicitud HTTP POST
    response = requests.post(base_url, data={'data': query})

    # Verifica si la respuesta fue exitosa
    if response.status_code != 200:
        return jsonify({"error": "Error en la solicitud a Overpass API"}), response.status_code

    # Retorna la respuesta JSON de Overpass API
    return jsonify(response.json())

class ErrorResponse:
    def __init__(self, error):
        self.error = error

@app.route('/parques', methods=['GET'])
def parques_handler():
    # Define la URL base de Overpass API
    base_url = "https://overpass-api.de/api/interpreter"

    # Define la consulta para los parques en las comunas específicas
    query = """
    [out:json];
    area["name"="Santiago"]["admin_level"="8"]->.santiago;
    area["name"="Providencia"]["admin_level"="8"]->.providencia;
    area["name"="Las Condes"]["admin_level"="8"]->.lascondes;
    area["name"="Ñuñoa"]["admin_level"="8"]->.nunoa;

    (
      node["leisure"="park"](area.santiago);
      node["leisure"="park"](area.providencia);
      node["leisure"="park"](area.lascondes);
      node["leisure"="park"](area.nunoa);
      way["leisure"="park"](area.santiago);
      way["leisure"="park"](area.providencia);
      way["leisure"="park"](area.lascondes);
      way["leisure"="park"](area.nunoa);
    );

    out body;
    >;
    out skel qt;
    """

    # Haz la solicitud HTTP POST
    response = requests.post(base_url, data={'data': query})

    # Verifica si la respuesta fue exitosa
    if response.status_code != 200:
        return jsonify(ErrorResponse("Error en la solicitud a Overpass API").__dict__), response.status_code

    # Lee el cuerpo de la respuesta
    body = response.json()

    # Configurar el tipo de contenido como JSON
    return jsonify(body)

@app.route('/museos', methods=['GET'])
def museos_handler():
    # Define la URL base de Overpass API
    base_url = "https://overpass-api.de/api/interpreter"

    # Define la consulta con el bounding box y los filtros
    query = f"""
    [out:json][timeout:25];
    nwr["tourism"="museum"]({MIN_LAT},{MIN_LON},{MAX_LAT},{MAX_LON});
    out geom;
    """

    # Haz la solicitud HTTP POST
    response = requests.post(base_url, data={'data': query})

    # Verifica si la respuesta fue exitosa
    if response.status_code != 200:
        return jsonify({"error": "Error en la solicitud a Overpass API"}), response.status_code

    # Lee el cuerpo de la respuesta
    body = response.json()

    # Aquí puedes insertar el GeoJSON en la base de datos utilizando una función como save_geojson_to_postgis(body)
    # err = save_geojson_to_postgis(body)
    # if err is not None:
    #     return jsonify({"error": "Error al insertar GeoJSON en PostGIS"}), 500

    # Configurar el tipo de contenido como JSON
    return jsonify(body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Cambiado a 0.0.0.0

