import os
import psycopg2
import json
from geoalchemy2 import Geometry, WKTElement
<<<<<<< HEAD:Sitio Web/backend/migration/load_geojson.py
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, String, inspect
=======
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, String, inspect, text
>>>>>>> rama-jassi:backend/migration/load_geojson.py
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker

# Datos de conexión a la base de datos
DB_NAME = os.getenv("POSTGRES_DB", "geodata")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
<<<<<<< HEAD:Sitio Web/backend/migration/load_geojson.py
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
=======
DB_HOST = os.getenv("POSTGRES_HOST", "postgis")
>>>>>>> rama-jassi:backend/migration/load_geojson.py
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Conexión usando SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

<<<<<<< HEAD:Sitio Web/backend/migration/load_geojson.py
=======
# Habilitar PostGIS
def enable_postgis():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))

# Llamada para habilitar PostGIS
enable_postgis()

>>>>>>> rama-jassi:backend/migration/load_geojson.py
# Función para convertir GeoJSON a WKT
def geojson_to_wkt(geometry):
    if geometry['type'] == 'Polygon':
        coordinates = geometry['coordinates'][0]
        wkt_coordinates = ", ".join([f"{lon} {lat}" for lon, lat in coordinates])
        return f"SRID=4326;POLYGON(({wkt_coordinates}))"
    elif geometry['type'] == 'MultiPolygon':
        multipolygon_parts = []
        for polygon in geometry['coordinates']:
            polygon_coordinates = polygon[0]
            wkt_coordinates = ", ".join([f"{lon} {lat}" for lon, lat in polygon_coordinates])
            multipolygon_parts.append(f"(({wkt_coordinates}))")
        return f"SRID=4326;MULTIPOLYGON({', '.join(multipolygon_parts)})"
    elif geometry['type'] == 'Point':
        lon, lat = geometry['coordinates']
        return f"SRID=4326;POINT({lon} {lat})"
    elif geometry['type'] == 'LineString':
        coordinates = geometry['coordinates']
        wkt_coordinates = ", ".join([f"{lon} {lat}" for lon, lat in coordinates])
        return f"SRID=4326;LINESTRING({wkt_coordinates})"
    else:
        raise ValueError(f"Tipo de geometría '{geometry['type']}' no soportado.")

# Función para cargar GeoJSON en la base de datos solo si la tabla no existe
def load_geojson_to_db(geojson_path, table_name):
    inspector = inspect(engine)

    # Verificar si la tabla ya existe
    if inspector.has_table(table_name):
        print(f"La tabla '{table_name}' ya existe. Se omite la creación e inserción de datos.")
        return

    # Crear tabla si no existe
    table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('properties', JSON),
        Column('geometry', Geometry('GEOMETRY', srid=4326)),
        extend_existing=True
    )
    metadata.create_all(engine)

    # Cargar los datos del archivo GeoJSON
    with open(geojson_path) as f:
        data = json.load(f)

    # Insertar datos en la tabla
    for feature in data['features']:
<<<<<<< HEAD:Sitio Web/backend/migration/load_geojson.py
        # Convertir la geometría a WKT
        geometry_wkt = geojson_to_wkt(feature['geometry'])
        geometry = WKTElement(geometry_wkt, srid=4326)
=======
        print("FEATURES: ", feature);
        # Convertir la geometría a WKT
        geometry_wkt = geojson_to_wkt(feature['geometry'])
        geometry = WKTElement(geometry_wkt, srid=4326)

        print("Geometry WKT:", geometry_wkt) 

        
>>>>>>> rama-jassi:backend/migration/load_geojson.py
        properties = feature['properties']
        ins = table.insert().values(properties=properties, geometry=geometry)
        session.execute(ins)

    session.commit()
    print(f"Datos insertados en la tabla '{table_name}'.")

# Lista de archivos GeoJSON y sus tablas correspondientes
geojson_files = [
    ('exportMuseos.geojson', 'museos'),
    ('exportIglesias.geojson', 'iglesias'),
    ('exportMonumentos.geojson', 'monumentos'),
    ('exportParques.geojson', 'parques'),
]

# Cargar cada archivo GeoJSON en la base de datos
for geojson_path, table_name in geojson_files:
    load_geojson_to_db(geojson_path, table_name)
<<<<<<< HEAD:Sitio Web/backend/migration/load_geojson.py

=======
    
>>>>>>> rama-jassi:backend/migration/load_geojson.py
# Cerrar sesión
session.close()
