import { Circle, Popup } from "react-leaflet";

interface CirculosProps {
    coordinates: [number, number][]; // Un arreglo de pares [x, y] en EPSG:3857
    color: string;
    radius: number; // Agregamos un radio para el círculo
}

// Función para convertir coordenadas EPSG:3857 a EPSG:4326
function epsg3857ToLatLon(x: number, y: number): [number, number] {
    const lon = (x * 180) / 20037508.34;
    const lat =
        (Math.atan(Math.exp(y * Math.PI / 20037508.34)) * 360) / Math.PI - 90;
    return [lat, lon];
}

export const Circulos = ({ coordinates, color, radius }: CirculosProps) => {
    return (
        <>
            {coordinates.map((coord, index) => {
                const [x, y] = coord; // Desestructuración de coordenadas

                // Convertir a lat/lon
                const [lat, lon] = epsg3857ToLatLon(x, y);

                return (
                    <Circle
                        key={index}
                        center={[lat, lon]}
                        radius={radius}
                        pathOptions={{ color }}
                    >
                        <Popup>
                            <b>Círculo {index + 1}</b><br />
                            Coordenadas: {`Lat: ${lat}, Lon: ${lon}`}
                        </Popup>
                    </Circle>
                );
            })}
        </>
    );
};
