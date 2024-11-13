import os
import json
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, Float, Boolean, inspect, text
from sqlalchemy.orm import sessionmaker
from shapely.geometry import shape

# Datos de conexión a la base de datos
DB_NAME = os.getenv("POSTGRES_DB", "geodata")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
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
        conn.execute(text("CREATE EXTENSION pgrouting;"))
    
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
        Column('source', Integer, nullable=False),  # Nodo de origen (Placeholder)
        Column('target', Integer, nullable=False),  # Nodo de destino (Placeholder)
        Column('cost', Float, nullable=False),      # Costo (distancia euclidiana)
        Column('oneway', Boolean, default=False),   # Si es unidireccional
        Column('geometry', Geometry('GEOMETRY', srid=4326)),  # Cambiado a GEOMETRY para aceptar ambos tipos
        extend_existing=True
    )
    metadata.create_all(engine)

    # Cargar los datos del archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Insertar calles en la tabla
    for feature in geojson_data['features']:
        geometry = shape(feature['geometry'])  # Convertir a objeto shapely
        geometry_wkt = geometry.wkt  # Obtener WKT
        geometry_element = WKTElement(geometry_wkt, srid=4326)

        properties = feature['properties']
        nodes = properties.get('nodes', [])  # Ajusta según cómo se almacenen los nodos

        # Calcular el costo como distancia euclidiana entre el primer y último nodo
        if len(nodes) >= 2:
            cost = euclidean_distance(nodes[0], nodes[-1])
        else:
            cost = 0  # O un valor por defecto

        # Verificar si la calle es unidireccional
        oneway = properties.get('oneway', 'no') == 'yes'

        # Insertar la calle en la tabla
        ins = calles_table.insert().values(
            source=1,  # Placeholder, se debe ajustar según tu modelo de nodos
            target=2,  # Placeholder, igual que el anterior
            cost=cost,
            oneway=oneway,
            geometry=geometry_element
        )
        session.execute(ins)

    session.commit()
    print("Datos insertados en la tabla 'calles'.")

# Ruta al archivo GeoJSON de calles
calles_geojson_path = 'roads_santiago.geojson'  # Cambia la extensión a .geojson

# Cargar las calles en la base de datos
enable_extensions()
check_extensions()

load_calles_from_geojson(calles_geojson_path)

# Cerrar la sesión
session.close()