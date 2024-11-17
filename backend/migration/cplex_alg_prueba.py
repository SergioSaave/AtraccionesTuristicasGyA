import json
import time
from docplex.mp.model import Model
from shapely.geometry import shape, LineString
from collections import defaultdict

# Ruta al archivo GeoJSON
geojson_file = "export.geojson"

# Configurar los nodos inicial y final
source_node_index = 0  # Índice del nodo fuente
target_node_index = 1  # Índice del nodo destino (ajusta según el rango del dataset)

# Cargar datos desde el archivo GeoJSON
print("Cargando datos desde el archivo GeoJSON...")
with open(geojson_file, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Procesar las aristas desde el archivo GeoJSON
print("Procesando las aristas desde el archivo...")
edges_dict = {}
nodes = set()

for feature in geojson_data["features"]:
    geom = shape(feature["geometry"])
    if isinstance(geom, LineString):
        properties = feature["properties"]
        edge_id = properties.get("id", len(edges_dict) + 1)  # Asigna un ID único si no existe
        source = tuple(geom.coords[0])  # Nodo fuente (coordenadas)
        target = tuple(geom.coords[-1])  # Nodo destino (coordenadas)
        cost = geom.length  # Longitud como costo

        # Solo agrega aristas válidas
        if source != target and cost > 0:
            edges_dict[edge_id] = {"source": source, "target": target, "cost": cost}
            nodes.add(source)
            nodes.add(target)

print(f"{len(edges_dict)} aristas procesadas y {len(nodes)} nodos únicos encontrados.")

# Seleccionar nodos inicial y final
nodes_list = list(nodes)
source_node = nodes_list[source_node_index]
target_node = nodes_list[target_node_index]
print(f"Nodo fuente: {source_node}, Nodo destino: {target_node}")

# Filtrar solo las aristas necesarias para conectar todos los nodos
# Inicialmente, incluimos todas las aristas
relevant_edges = edges_dict
print(f"{len(relevant_edges)} aristas consideradas para el modelo.")

# Construir el modelo de optimización
print("Construyendo el modelo de optimización...")
mdl = Model(name="Ruta más corta")

# Variables de decisión
edge_vars = {edge_id: mdl.binary_var(name=f"edge_{edge_id}") for edge_id in relevant_edges}
print(f"Se definieron {len(edge_vars)} variables de decisión.")

# Función objetivo
print("Definiendo la función objetivo...")
mdl.minimize(mdl.sum(edge_vars[edge_id] * relevant_edges[edge_id]["cost"] for edge_id in relevant_edges))
print("Función objetivo definida.")

# Restricciones de flujo
print("Definiendo restricciones de flujo...")
incoming_edges = defaultdict(list)
outgoing_edges = defaultdict(list)

for edge_id, edge in relevant_edges.items():
    incoming_edges[edge["target"]].append(edge_id)
    outgoing_edges[edge["source"]].append(edge_id)

for node in nodes:
    if node == source_node:
        mdl.add_constraint(
            mdl.sum(edge_vars[eid] for eid in outgoing_edges[node])
            - mdl.sum(edge_vars[eid] for eid in incoming_edges[node]) == 1
        )
    elif node == target_node:
        mdl.add_constraint(
            mdl.sum(edge_vars[eid] for eid in incoming_edges[node])
            - mdl.sum(edge_vars[eid] for eid in outgoing_edges[node]) == 1
        )
    else:
        mdl.add_constraint(
            mdl.sum(edge_vars[eid] for eid in incoming_edges[node])
            == mdl.sum(edge_vars[eid] for eid in outgoing_edges[node])
        )

print("Restricciones de flujo definidas.")

# Resolver el modelo
print("Resolviendo el modelo...")
mdl.context.solver.log_output = True  # Habilitar logs de CPLEX
solution = mdl.solve()

# Verificar la solución
if solution:
    print("Ruta más corta encontrada.")
    route_edges = [edge_id for edge_id in edge_vars if edge_vars[edge_id].solution_value > 0.5]

    # Calcular distancia total
    distancia_total = sum(relevant_edges[edge_id]["cost"] for edge_id in route_edges)
    print(f"Distancia total de la ruta: {distancia_total} unidades.")

    # Exportar la ruta a GeoJSON
    features = []
    for edge_id in route_edges:
        edge = relevant_edges[edge_id]
        line = LineString([edge["source"], edge["target"]])
        features.append({
            "type": "Feature",
            "properties": {"id": edge_id},
            "geometry": json.loads(line.to_json())
        })

    geojson_result = {
        "type": "FeatureCollection",
        "features": features
    }

    geojson_path = "ruta_mas_corta.geojson"
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson_result, f, ensure_ascii=False, indent=4)

    print(f"Ruta exportada a {geojson_path}.")
else:
    print("No se encontró una solución óptima.")
