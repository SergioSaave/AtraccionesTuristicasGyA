import folium
import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify
from shapely.wkt import loads  # Asegúrate de importar 'loads' de shapely

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'dbname': 'geodata',
    'user': 'postgres',
    'password': 'password',
    'host': 'postgres',
    'port': '5432'
}

def get_route(source_id, target_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    query = """
    SELECT c.id, c.source, c.target, c.cost, ST_AsText(c.geometry)
    FROM pgr_dijkstra(
        'SELECT id, source, target, cost FROM calles',
        %s,
        %s,
        false
    ) AS r
    JOIN calles AS c ON r.edge = c.id;
    """
    cur.execute(query, (source_id, target_id))
    edges = cur.fetchall()
    conn.close()
    return edges

def create_map(edges):
    m = folium.Map(location=[-33.4489, -70.6693], zoom_start=13)

    if not edges:
        print("No se encontraron bordes para la ruta.")
        return None

    for edge in edges:
        edge_id, source, target, cost, geom_wkt = edge
        geom = loads(geom_wkt) 
        coords = list(geom.coords)

        folium.PolyLine(locations=[(lat, lon) for lon, lat in coords], color='blue', weight=2, opacity=0.7).add_to(m)

    m.save("ruta_map.html")
    print("El mapa se ha guardado como 'ruta_map.html'.")
    
    return edges 

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/route/<int:source_id>/<int:target_id>', methods=['GET'])
def route(source_id, target_id):
    try:
        route = get_route(source_id, target_id)
        
        if not route:
            return jsonify({"error": "No route found."}), 404
        
        # Crear y guardar el mapa con la ruta
        create_map(route)

        return jsonify(route)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
