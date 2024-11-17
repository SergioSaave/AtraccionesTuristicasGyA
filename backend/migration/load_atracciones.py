import json
import psycopg2
from psycopg2 import sql
import os
from shapely.geometry import shape, Point
from shapely import wkt
from shapely.geometry import LineString

# Parámetros de conexión
db_params = {
    "host": os.getenv("DB_HOST", "postgis"),
    "dbname": os.getenv("DB_NAME", "geodata"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Crear/verificar la tabla 'atracciones'
cur.execute("""
    CREATE TABLE IF NOT EXISTS atracciones (
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        tipo TEXT,
        nodo_id INTEGER REFERENCES nodos(id),
        geom GEOMETRY(Point, 4326)
    );
""")
print("Tabla 'atracciones' creada/verificada.")

# Limpiar la tabla 'atracciones'
cur.execute("DELETE FROM atracciones;")
print("Tabla 'atracciones' limpiada antes de la inserción.")

# Consultas SQL
insert_node_query = sql.SQL("""
    INSERT INTO nodos (geom)
    VALUES (ST_GeomFromText(%s, 4326))
    RETURNING id
""")
insert_edge_query = sql.SQL("""
    INSERT INTO aristas (source, target, cost, reverse_cost, geom)
    VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326))
""")
insert_attraction_query = sql.SQL("""
    INSERT INTO atracciones (nombre, tipo, nodo_id, geom)
    VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))
""")

# Encuentra el nodo más cercano a un punto
def find_nearest_node(point_wkt):
    cur.execute("""
        SELECT id, ST_Distance(geom, ST_GeomFromText(%s, 4326)) AS distance
        FROM nodos
        ORDER BY distance
        LIMIT 1
    """, (point_wkt,))
    return cur.fetchone()

# Procesar atracciones turísticas
geojson_files = [
    {"path": "metadataOverpassParques.geojson", "type": "Parque"},
    {"path": "metadataOverpassMuseos.geojson", "type": "Museo"},
    {"path": "metadataOverpassMonumentos.geojson", "type": "Monumento"},
    {"path": "metadataOverpassIglesias.geojson", "type": "Iglesia"},
]

# Contador de atracciones añadidas
counter = 0

for file_info in geojson_files:
    print(f"Procesando archivo: {file_info['path']} de tipo {file_info['type']}")
    try:
        with open(file_info["path"], 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        # Validar estructura del archivo
        if 'elements' not in geojson_data:
            print(f"Error: El archivo {file_info['path']} no contiene la clave 'elements'.")
            continue
        
        print(f"Archivo {file_info['path']} cargado exitosamente con {len(geojson_data['elements'])} elementos.")

        for idx, element in enumerate(geojson_data['elements']):
            if element['type'] == 'node':  # Nos interesan los nodos
                lat = element.get('lat')
                lon = element.get('lon')
                tags = element.get('tags', {})
                nombre = tags.get('name', 'Sin Nombre')

                # Crear geometría a partir de latitud y longitud
                geom = Point(lon, lat)
                nearest_node = find_nearest_node(geom.wkt)

                if nearest_node:
                    nearest_node_id, distance = nearest_node
                    
                    # Insertar el lugar turístico como un nodo
                    cur.execute(insert_node_query, (geom.wkt,))
                    attraction_node_id = cur.fetchone()[0]
                    print(f"Nodo insertado: {attraction_node_id}, nombre: '{nombre}'")

                    # Crear una arista como LINESTRING al nodo más cercano
                    cur.execute("SELECT ST_AsText(geom) FROM nodos WHERE id = %s", (nearest_node_id,))
                    nearest_node_geom = cur.fetchone()[0]
                    line_geom = LineString([geom, wkt.loads(nearest_node_geom)]).wkt
                    print(f"Creando arista: {attraction_node_id} -> {nearest_node_id}, distancia: {distance}, geometría: {line_geom}")

                    # Insertar la arista con reverse_cost igual a cost
                    cur.execute(insert_edge_query, (
                        attraction_node_id, nearest_node_id, distance, distance, line_geom
                    ))
                    print(f"Arista insertada: {attraction_node_id} -> {nearest_node_id}")

                    # Insertar en la tabla de atracciones
                    cur.execute(insert_attraction_query, (nombre, file_info["type"], attraction_node_id, geom.wkt))
                    print(f"Atracción '{nombre}' insertada como nodo {attraction_node_id} con una arista hacia {nearest_node_id}.")

                    # Incrementar el contador y mostrar un mensaje cada 100 inserciones
                    counter += 1
                    if counter % 100 == 0:
                        print(f"{counter} atracciones añadidas hasta ahora.")
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo {file_info['path']}. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: El archivo {file_info['path']} no está en formato JSON válido. {e}")
    except Exception as e:
        print(f"Error inesperado al procesar el archivo {file_info['path']}: {e}")
        conn.rollback()  # Revertir la transacción para evitar bloqueos futuros

# Reindexar después de las inserciones
cur.execute("REINDEX TABLE nodos;")
cur.execute("REINDEX TABLE aristas;")
print("Índices actualizados.")

# Confirmar los cambios
conn.commit()
print("Atracciones insertadas correctamente.")
print(f"Total de atracciones añadidas: {counter}")
cur.close()
conn.close()
