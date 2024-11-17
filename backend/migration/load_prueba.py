import json
import psycopg2
from psycopg2 import sql
import os
from shapely.geometry import shape, Point, LineString
from shapely import wkt


db_params = {
    "host": os.getenv("DB_HOST", "postgis"),
    "dbname": os.getenv("DB_NAME", "geodata"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}
conn = psycopg2.connect(**db_params)
cur = conn.cursor()


with open('export.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)


# Consultas para insertar nodos y aristas
insert_node_query = sql.SQL("""
    INSERT INTO nodos (geom)
    VALUES (ST_GeomFromText(%s, 4326))
    RETURNING id
""")

insert_edge_query = sql.SQL("""
    INSERT INTO aristas (source, target, cost, geom)
    VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))
""")

# Almacén para nodos existentes
cur.execute("SELECT id, ST_AsText(geom) FROM nodos")
all_nodes_in_db = {wkt.loads(geom_wkt): node_id for node_id, geom_wkt in cur.fetchall()}

# Función para insertar o recuperar un nodo
def insert_node_if_not_exists(point_geom):
    if point_geom in all_nodes_in_db:
        return all_nodes_in_db[point_geom]
    else:
        cur.execute(insert_node_query, (point_geom.wkt,))
        node_id = cur.fetchone()[0]
        all_nodes_in_db[point_geom] = node_id
        return node_id

# Procesar las líneas del archivo GeoJSON
for idx,feature in enumerate(geojson_data['features']):
    print("nodo:",idx," insertado")
    geom = shape(feature['geometry'])
    if isinstance(geom, LineString):
        start_point = Point(geom.coords[0])
        end_point = Point(geom.coords[-1])

        source_node_id = insert_node_if_not_exists(start_point)
        target_node_id = insert_node_if_not_exists(end_point)

        cost = geom.length  # Utiliza la longitud de la línea como coste
        cur.execute(insert_edge_query, (
            source_node_id, target_node_id, cost, geom.wkt
        ))

conn.commit()



print("Consulta LISTA...")
cur.close()
conn.close()