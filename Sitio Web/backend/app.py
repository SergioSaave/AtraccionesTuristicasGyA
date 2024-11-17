from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # Importa CORS
import cv2
import numpy as np
import requests
import os
from dotenv import load_dotenv
import json
import openai
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import RealDictCursor  # Asegúrate de importar RealDictCursor


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

def load_image_from_path(path):
    try:
        # Cargar imagen usando OpenCV
        img = cv2.imread(path)
        return img
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

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
    # url = "https://stop.carabineros.cl/geoserver/stop/wms/?service=WMS&request=GetMap&version=1.1.1&layers=stop%3ADelitosMayorConnotacionSocial&styles=&format=image%2Fpng&transparent=true&info_format=application%2Fjson&width=3750&height=2904&srs=EPSG%3A3857&bbox=-7884785.215729073%2C-3969088.2399931327%2C-7848955.358720397%2C-3941341.5987256127"
    image_path = "./amenaza.png"  # Asegúrate de poner el nombre correcto de la imagen
    
    # Carga la imagen desde la ruta local
    img = load_image_from_path(image_path)
    
    # Carga la imagen desde la URL
    # img = load_image_from_url(url)
    
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

load_dotenv()  # Asegúrate de cargar el .env al inicio del script

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = "https://www.googleapis.com/customsearch/v1"

if not API_KEY or not SEARCH_ENGINE_ID or not OPENAI_API_KEY:
    raise ValueError("Las claves API no se han cargado correctamente desde el archivo .env")

ENDPOINT = "https://www.googleapis.com/customsearch/v1"

# Función para hacer una búsqueda en Google usando Custom Search API
def buscar_en_google(query):
    print(f"Realizando búsqueda en Google con la consulta: {query}")
    
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'siteSearch': '.cl',  # Filtrar para dominios de Chile
        'siteSearchFilter': 'i'  # Incluir solo resultados del dominio especificado
    }
    
    response = requests.get(ENDPOINT, params=params)
    response.raise_for_status()
    search_results = response.json()
    
    print("Resultados obtenidos de Google Custom Search:")
    print(json.dumps(search_results, indent=4, ensure_ascii=False))
    
    return search_results

# Función para extraer el HTML de una página web con encabezado 'User-Agent' para evitar el error 406
def obtener_contenido_pagina(url):
    try:
        print(f"Extrayendo contenido de la página: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)  # Tiempo de espera de 10 segundos
        response.raise_for_status()  # Lanza una excepción en caso de fallo
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()[:5000]  # Limitar a los primeros 5000 caracteres para evitar exceder tokens
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página {url}: {e}")
        return None

# Función para procesar la información con GPT-3.5 o GPT-4 y retornarla en formato JSON
def analizar_con_gpt(contenido, url, nombre_museo):
    openai.api_key = OPENAI_API_KEY
    
    messages = [
        {"role": "system", "content": f"Eres un asistente experto en análisis de sitios web para información de {nombre_museo}. Debes analizar solo páginas que coincidan con el nombre del museo."},
        {"role": "user", "content": f"Analiza esta página sobre {nombre_museo}: {url}\n\nContenido:\n{contenido}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        temperature=0,
        max_tokens=500
    )
    
    respuesta_gpt = response['choices'][0]['message']['content']

    resultado_json = {
        "abierto": "sí" in respuesta_gpt.lower(),
        "silla_ruedas": "accesibilidad para sillas de ruedas" in respuesta_gpt.lower(),
        "Braille": "sistema braille" in respuesta_gpt.lower(),
        "open_festivos": "días festivos" in respuesta_gpt.lower(),
        "pet_friendly": "pet-friendly" in respuesta_gpt.lower() or "mascotas" in respuesta_gpt.lower()
    }

    return resultado_json

# Endpoint para buscar y analizar información de museos
@app.route('/buscar-museo', methods=['GET'])
def buscar_y_analizar_museo():
    # Obtener el parámetro 'nombre_museo' de la URL de la solicitud GET
    nombre_museo = request.args.get('nombre_museo', default='', type=str)
    
    if not nombre_museo:
        return jsonify({"error": "Se requiere un nombre de museo"}), 400

    query = f"{nombre_museo} accesibilidad sillas de ruedas abierto hoy teléfono"
    resultados = buscar_en_google(query)
    
    # Limitar a los 3 primeros resultados
    urls = [item['link'] for item in resultados.get('items', [])[:3] if '.cl' in item['link']]
    
    resultados_analizados = []

    # Extraer y procesar el contenido de cada página
    for url in urls:
        contenido_pagina = obtener_contenido_pagina(url)
        if contenido_pagina:
            # Enviar el contenido a GPT para su análisis
            resultado_gpt = analizar_con_gpt(contenido_pagina, url, nombre_museo)
            resultados_analizados.append({
                "url": url,
                "resultado": resultado_gpt
            })

    return jsonify(resultados_analizados)

@app.route('/calcular-tiempo-ruta', methods=['POST'])
def calcular_tiempo_ruta_optima():
    activities = request.json.get('activities', [])
    
    if not activities or len(activities) < 2:
        return jsonify({"error": "Se requieren al menos dos actividades con coordenadas"}), 400

    total_time = 0
    rutas = []

    # Calcular rutas entre actividades utilizando OSRM
    for i in range(len(activities) - 1):
        coord1 = activities[i].split(',')
        coord2 = activities[i + 1].split(',')

        # Llamada a la API de OSRM para calcular el tiempo de viaje
        url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=false"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            travel_time = data['routes'][0]['duration'] / 60  # Convertir a minutos
            total_time += travel_time

            # Obtener la ruta en formato GeoJSON o como lista de coordenadas
            ruta = data['routes'][0]['geometry']
            rutas.append({
                "desde": activities[i],
                "hasta": activities[i + 1],
                "tiempo": round(travel_time, 2),
                "ruta": ruta
            })
        else:
            return jsonify({"error": "Error al calcular la ruta"}, status=500)

    return jsonify({
        "total_time": round(total_time, 2),
        "rutas": rutas
    })
    
def get_db_connection():
    connection = psycopg2.connect(
        host='postgis',  # Puede ser el nombre del contenedor de PostgreSQL o el alias de red
        database='geodata',
        user='postgres',
        password='password',
        port=5432  # El puerto por defecto de PostgreSQL
    )
    return connection

# Nuevo endpoint para consultar la base de datos
from flask import request

@app.route('/consultar-datos', methods=['GET'])
def consultar_datos():
    # Obtener latitud y longitud de los parámetros de la solicitud
    lat_inicio = float(request.args.get('lat_inicio'))
    lon_inicio = float(request.args.get('lon_inicio'))
    lat_fin = float(request.args.get('lat_fin'))
    lon_fin = float(request.args.get('lon_fin'))

    # Conectar a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Buscar el ID del nodo más cercano a la coordenada de inicio
    cursor.execute("""
        SELECT id
        FROM nodos
        ORDER BY ST_Distance(geom, ST_SetSRID(ST_Point(%s, %s), 4326)) 
        LIMIT 1;
    """, (lon_inicio, lat_inicio))
    nodo_inicio = cursor.fetchone()[0]
    
    # Buscar el ID del nodo más cercano a la coordenada de fin
    cursor.execute("""
        SELECT id
        FROM nodos
        ORDER BY ST_Distance(geom, ST_SetSRID(ST_Point(%s, %s), 4326)) 
        LIMIT 1;
    """, (lon_fin, lat_fin))
    nodo_fin = cursor.fetchone()[0]
    
    # Nueva consulta SQL con los nodos calculados
    query = """
        SELECT 
            dijkstra.seq,
            dijkstra.node,
            ST_Y(nodos.geom) AS latitude,
            ST_X(nodos.geom) AS longitude
        FROM 
            pgr_dijkstra(
                'SELECT id, source, target, cost FROM aristas',
                %s,  -- Nodo inicial
                %s, -- Nodo final
                TRUE
            ) AS dijkstra
        JOIN 
            nodos
        ON 
            dijkstra.node = nodos.id
        ORDER BY 
            dijkstra.seq;
    """
    
    # Ejecutar la consulta con los nodos de inicio y fin
    cursor.execute(query, (nodo_inicio, nodo_fin))
    
    # Obtener los resultados
    resultados = cursor.fetchall()
    
    # Cerrar la conexión
    cursor.close()
    connection.close()
    
    # Retornar los resultados como JSON
    return jsonify(resultados)

@app.route('/nodo-mas-cercano', methods=['GET'])
def nodo_mas_cercano():
    # Obtener latitud y longitud de los parámetros de consulta
    latitud = float(request.args.get('latitud'))
    longitud = float(request.args.get('longitud'))
    
    # Conectar a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    # Consulta SQL para encontrar el nodo más cercano
    query = """
        SELECT 
          id,
          ST_AsText(geom) AS geom,
          ST_Distance(geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) AS distance
        FROM 
          nodos
        ORDER BY 
          distance
        LIMIT 1;
    """
    
    # Ejecutar la consulta con los parámetros latitud y longitud
    cursor.execute(query, (longitud, latitud))
    
    # Obtener el nodo más cercano
    resultado = cursor.fetchone()
    
    # Cerrar la conexión
    cursor.close()
    connection.close()
    
    # Retornar el nodo más cercano como JSON
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({'error': 'No se encontró un nodo cercano'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Cambiado a 0.0.0.0