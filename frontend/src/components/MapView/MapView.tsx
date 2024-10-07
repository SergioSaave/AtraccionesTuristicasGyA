import { useEffect, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { Overpass } from '../../interfaces/overpass.interface';
import data from '../../../museos.json'

interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: {
        [key: string]: string | undefined; // Etiquetas con campos opcionales
    };
}

const overpassData = data;

export const MapView = () => {

    const [nodes, setNodes] = useState<Node[]>([]);

    useEffect(() => {
        // Simulamos cargar los datos desde un archivo JSON
        const nodesData = overpassData.elements.filter(element => element.type === 'node') as Node[];
        setNodes(nodesData);
    }, []);

    return (
        <MapContainer center={[-33.447487, -70.673676]} zoom={12} style={{ height: "100%", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {nodes.map((node) => (
                <Marker key={node.id} position={[node.lat, node.lon]}>
                    <Popup>
                        <b>{node.tags?.name || 'Sin nombre'}</b><br />
                        Amenity: {node.tags?.amenity || 'Desconocido'}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    )
}
