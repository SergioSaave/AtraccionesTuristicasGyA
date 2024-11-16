CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION pgrouting;



CREATE TABLE IF NOT EXISTS nodos (
    id SERIAL PRIMARY KEY,
    geom Geometry(Point, 4326)
);


CREATE TABLE IF NOT EXISTS aristas (
    id SERIAL PRIMARY KEY,
    source INTEGER NOT NULL,
    target INTEGER NOT NULL,
    cost FLOAT NOT NULL,
    reverse_cost FLOAT,
    geom Geometry(LineString, 4326),
    lanes INTEGER DEFAULT 1,
    oneway VARCHAR(10) DEFAULT 'no' -- Ampliar el tamaño para valores como 'reversible'
);




-- ogr2ogr -f PostgreSQL PG:"host=localhost user=postgres password=postgres dbname=gis port=25432" ./accidentes.geojson -nln accidentes -lco GEOMETRY_NAME=geom -lco FID=FID