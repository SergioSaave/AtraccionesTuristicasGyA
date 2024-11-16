CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION pgrouting;



CREATE TABLE IF NOT EXISTS nodos (
  id SERIAL PRIMARY KEY,
  geom GEOMETRY(Point, 4326)
);

CREATE TABLE IF NOT EXISTS aristas (
  id SERIAL PRIMARY KEY,
  source INTEGER,
  target INTEGER,
  cost DOUBLE PRECISION,
  reverse_cost DOUBLE PRECISION,
  geom GEOMETRY(LineString, 4326)
);


-- ogr2ogr -f PostgreSQL PG:"host=localhost user=postgres password=postgres dbname=gis port=25432" ./accidentes.geojson -nln accidentes -lco GEOMETRY_NAME=geom -lco FID=FID