import sqlite3
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection

def connect_to_sqlite(db_file):
    """Conectar a la base de datos SQLite"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos SQLite: {e}")
        return None

def fetch_data(conn, table_name):
    """Obtener datos de la tabla SQLite"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Obtener nombres de columnas
        column_names = [description[0] for description in cursor.description]

        # Convertir las filas (tuplas) en diccionarios
        data = [dict(zip(column_names, row)) for row in rows]

        return data
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la tabla {table_name}: {e}")
        return []

def import_to_elasticsearch(es, index_name, data):
    """Importar datos a Elasticsearch"""
    try:
        helpers.bulk(es, data, index=index_name)
        print(f"Datos importados correctamente a Elasticsearch en el índice {index_name}")
    except Exception as e:
        print(f"Error al importar datos a Elasticsearch en el índice {index_name}: {e}")

def main():
    # Configuración de Elasticsearch
    es = Elasticsearch(hosts=[{"host": "host.docker.internal", "port": 9200}], connection_class=RequestsHttpConnection, max_retries=30, retry_on_timeout=True, request_timeout=30)

    # Configuración de SQLite
    db_file = 'datasalas-new.db'  # Nombre del archivo SQLite
    table_names = ['buildings', 'courses', 'rooms', 'schedules', 'sections', 'teachers']  # Lista de tablas a importar

    # Conectar a SQLite
    conn = connect_to_sqlite(db_file)
    if not conn:
        return

    for table_name in table_names:
        # Obtener datos de SQLite
        data = fetch_data(conn, table_name)
        if not data:
            print(f"No se encontraron datos para importar de la tabla {table_name}")
            continue

        # Nombre del índice en Elasticsearch
        index_name = f'{table_name}_index'

        # Importar datos a Elasticsearch
        import_to_elasticsearch(es, index_name, data)

    # Cerrar conexión SQLite
    conn.close()

if __name__ == "__main__":
    main()