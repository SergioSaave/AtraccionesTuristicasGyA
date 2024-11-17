import requests
import json

# URL base de la API de Overpass
base_url = "https://overpass-api.de/api/interpreter"

# Define las coordenadas del bounding box
min_lat = -33.54912050860342  # Límite sur
min_lon = -70.79795837402345  # Límite oeste
max_lat = -33.35834837283271  # Límite norte
max_lon = -70.52639007568361  # Límite este

# Define la consulta para lugares de culto cristianos
worship_query = f"""
[out:json][timeout:25];
nwr["amenity"="place_of_worship"]["religion"="christian"]({min_lat},{min_lon},{max_lat},{max_lon});
out geom;
"""

# Define la consulta para monumentos históricos
monument_query = f"""
[out:json][timeout:25];
nwr["historic"="monument"]({min_lat},{min_lon},{max_lat},{max_lon});
out geom;
"""

# Define la consulta para museos
museum_query = f"""
[out:json][timeout:25];
nwr["tourism"="museum"]({min_lat},{min_lon},{max_lat},{max_lon});
out geom;
"""

# Define la consulta para parques en Santiago, Providencia, Las Condes y Ñuñoa
park_query = """
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

def fetch_overpass_data(query, filename):
    # Realiza la solicitud POST a la API de Overpass con la consulta
    response = requests.post(base_url, data={"data": query})

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Cargar la respuesta en formato JSON
        response_json = response.json()
        
        # Guardar la respuesta JSON en un archivo
        with open(filename, 'w') as json_file:
            json.dump(response_json, json_file, indent=4)
        
        print(f"Consulta realizada con éxito. El JSON ha sido guardado en '{filename}'.")
    else:
        print(f"Error en la solicitud para {filename}. Código de estado: {response.status_code}")

# Descargar y guardar la información de lugares de culto cristianos
fetch_overpass_data(worship_query, 'metadataOverpassIglesias.json')

# Descargar y guardar la información de monumentos históricos
fetch_overpass_data(monument_query, 'metadataOverpassMonumentos.json')

# Descargar y guardar la información de museos
fetch_overpass_data(museum_query, 'metadataOverpassMuseos.json')

# Descargar y guardar la información de parques
fetch_overpass_data(park_query, 'metadataOverpassParques.json')
