import os
import psycopg2
from docplex.mp.model import Model
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv(dotenv_path='.env')

# Parámetros de conexión a la base de datos
db_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": "25432",  # Cambiar según el puerto mapeado
    "dbname": "geodata",
    "user": "postgres",
    "password": "password",
}

# Mediciones de tiempo
start_time = time.time()

# Conexión a la base de datos
print("Conectando a la base de datos...")
conn = psycopg2.connect(**db_params)
cur = conn.cursor()
print("Conexión establecida. Tiempo: {:.2f} segundos".format(time.time() - start_time))

# Obtener IDs de los nodos de inicio y fin
source_id = 1  # Nodo inicial
target_id = 2  # Nodo final

# Consultar las aristas desde la base de datos
start_time = time.time()
print("Consultando las aristas desde la base de datos...")
cur.execute("""
    SELECT id, source, target, cost 
    FROM aristas
""")
edges = cur.fetchall()
print(f"{len(edges)} aristas obtenidas. Tiempo: {time.time() - start_time:.2f} segundos")

# Crear un diccionario con los datos de las aristas
start_time = time.time()
print("Procesando datos de las aristas...")
edges_dict = {edge[0]: {"source": edge[1], "target": edge[2], "cost": edge[3]} for edge in edges}
print(f"Datos de aristas procesados. Tiempo: {time.time() - start_time:.2f} segundos")

# Construir el modelo de optimización
start_time = time.time()
print("Construyendo el modelo de optimización...")
mdl = Model(name="Ruta más corta")

# Variables de decisión
print("Definiendo variables de decisión...")
edge_vars = {edge_id: mdl.binary_var(name=f"edge_{edge_id}") for edge_id in edges_dict}
print(f"Se definieron {len(edge_vars)} variables de decisión. Tiempo: {time.time() - start_time:.2f} segundos")

# Función objetivo
start_time = time.time()
print("Definiendo la función objetivo...")
mdl.minimize(mdl.sum(edge_vars[edge_id] * edges_dict[edge_id]["cost"] for edge_id in edges_dict))
print(f"Función objetivo definida. Tiempo: {time.time() - start_time:.2f} segundos")

# Restricciones de flujo
start_time = time.time()
print("Definiendo restricciones de flujo...")
nodes = set(edge["source"] for edge in edges_dict.values()).union(edge["target"] for edge in edges_dict.values())

for i, node in enumerate(nodes, start=1):
    if i % 100 == 0:  # Muestra el progreso cada 1000 nodos
        print(f"Procesando nodo {i}/{len(nodes)}...")

    incoming = [edge_id for edge_id in edges_dict if edges_dict[edge_id]["target"] == node]
    outgoing = [edge_id for edge_id in edges_dict if edges_dict[edge_id]["source"] == node]

    if node == source_id:
        mdl.add_constraint(mdl.sum(edge_vars[e] for e in outgoing) - mdl.sum(edge_vars[e] for e in incoming) == 1)
    elif node == target_id:
        mdl.add_constraint(mdl.sum(edge_vars[e] for e in incoming) - mdl.sum(edge_vars[e] for e in outgoing) == 1)
    else:
        mdl.add_constraint(mdl.sum(edge_vars[e] for e in incoming) == mdl.sum(edge_vars[e] for e in outgoing))
print(f"Restricciones de flujo definidas. Tiempo: {time.time() - start_time:.2f} segundos")

# Resolver el modelo
start_time = time.time()
print("Resolviendo el modelo...")
mdl.context.solver.log_output = True  # Habilitar logs de CPLEX
solution = mdl.solve()
print(f"Modelo resuelto. Tiempo: {time.time() - start_time:.2f} segundos")

# Verificar la solución
if solution:
    print("Ruta más corta encontrada.")
    route_edges = [edge_id for edge_id in edge_vars if edge_vars[edge_id].solution_value > 0.5]

    # Calcular distancia total
    distancia_total = sum(edges_dict[edge_id]["cost"] for edge_id in route_edges)
    print(f"Distancia total de la ruta: {distancia_total} unidades.")

    # Exportar la ruta a GeoJSON
    features = []
    for edge_id in route_edges:
        cur.execute("""
            SELECT ST_AsGeoJSON(geom) AS geometry 
            FROM aristas 
            WHERE id = %s
        """, (edge_id,))
        geom_json = cur.fetchone()[0]
        features.append({
            "type": "Feature",
            "properties": {"id": edge_id},
            "geometry": geom_json
        })

    geojson_result = {
        "type": "FeatureCollection",
        "features": features
    }

    geojson_path = "ruta_mas_corta.geojson"
    with open(geojson_path, "w", encoding="utf-8") as f:
        import json
        json.dump(geojson_result, f, ensure_ascii=False, indent=4)

    print(f"Ruta exportada a {geojson_path}.")
else:
    print("No se encontró una solución óptima.")

# Cerrar la conexión a la base de datos
cur.close()
conn.close()
