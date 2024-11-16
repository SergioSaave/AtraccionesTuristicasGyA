import os
import json
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, Float, Boolean, inspect, text
from sqlalchemy.orm import sessionmaker
from shapely.geometry import shape, LineString, Polygon, mapping

# Datos de conexión a la base de datos
DB_NAME = os.getenv("POSTGRES_DB", "geodata")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgis")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Conexión usando SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

def enable_extensions():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgrouting;"))
    
def check_extensions():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT extname FROM pg_extension;")).fetchall()
        extensions = {row[0] for row in result}
        print("Extensiones habilitadas:")
        print(extensions)
        if 'postgis' in extensions:
            print("PostGIS está habilitado.")
        else:
            print("PostGIS NO está habilitado.")
        
        if 'pgrouting' in extensions:
            print("pgRouting está habilitado.")
        else:
            print("pgRouting NO está habilitado.")

# Función para calcular la distancia euclidiana entre dos puntos (nodo inicial y final)
def euclidean_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5

def load_calles_from_geojson(geojson_path):
    inspector = inspect(engine)

    # Verificar si la tabla 'calles' ya existe
    if inspector.has_table('calles'):
        print("La tabla 'calles' ya existe. Se omite la creación e inserción de datos.")
        return

    # Crear la tabla 'calles'
    calles_table = Table(
        'calles', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('source', Integer, nullable=False),  # Nodo de origen
        Column('target', Integer, nullable=False),  # Nodo de destino
        Column('cost', Float, nullable=False),      # Costo (distancia euclidiana)
        Column('oneway', Boolean, default=False),   # Si es unidireccional
        Column('geometry', Geometry('GEOMETRY', srid=4326)),  # Cambiado a GEOMETRY para aceptar ambos tipos
        extend_existing=True
    )
    metadata.create_all(engine)

    # Cargar los datos del archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Generar IDs únicos para nodos y segmentos
    node_id_counter = 1
    node_mapping = {}  # Almacenar coordenadas de nodos y asignarles un ID único

    # Procesar cada feature
    for feature in geojson_data['features']:
        geometry = shape(feature['geometry'])
        
        # Si la geometría es un polígono, extraer los bordes y convertirlos en LineStrings
        if isinstance(geometry, Polygon):
            line_segments = [LineString([geometry.exterior.coords[i], geometry.exterior.coords[i+1]])
                             for i in range(len(geometry.exterior.coords) - 1)]
        elif isinstance(geometry, LineString):
            line_segments = [geometry]  # Si es LineString, usarlo directamente
        else:
            continue  # Omitir otros tipos de geometría

        # Insertar cada segmento como calle en la base de datos
        for segment in line_segments:
            start, end = segment.coords[0], segment.coords[-1]

            # Verificar si los puntos de inicio y fin ya tienen un ID asignado
            if start not in node_mapping:
                node_mapping[start] = node_id_counter
                node_id_counter += 1
            if end not in node_mapping:
                node_mapping[end] = node_id_counter
                node_id_counter += 1

            source = node_mapping[start]
            target = node_mapping[end]
            cost = euclidean_distance(start, end)

            # Convertir a WKT para almacenar en la base de datos
            geometry_wkt = segment.wkt
            geometry_element = WKTElement(geometry_wkt, srid=4326)

            # Insertar en la tabla
            ins = calles_table.insert().values(
                source=source,
                target=target,
                cost=cost,
                oneway=feature['properties'].get('oneway', 'no') == 'yes',
                geometry=geometry_element
            )
            session.execute(ins)

    session.commit()
    print("Datos insertados en la tabla 'calles'.")

# Ruta al archivo GeoJSON de calles
calles_geojson_path = 'export.geojson'  # Cambia la extensión a .geojson

# Cargar las calles en la base de datos
enable_extensions()
check_extensions()

load_calles_from_geojson(calles_geojson_path)

# Cerrar la sesión
session.close()
