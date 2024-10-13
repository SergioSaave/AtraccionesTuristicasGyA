import { useEffect, useState } from "react";
import { Marker, Popup } from "react-leaflet"
import data from '../../../museos.json'

interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: {
        [key: string]: string | undefined;
    };
}

const overpassData = data;

export const Marcador = () => {

    const [nodes, setNodes] = useState<Node[]>([]);

    useEffect(() => {
        // Simulamos cargar los datos desde un archivo JSON
        const nodesData = overpassData.elements.filter(element => element.type === 'node') as Node[];
        setNodes(nodesData);
    }, []);

    return (
        <>
            {
                nodes.map((node) => (
                    <Marker key={node.id} position={[node.lat, node.lon]}>
                        <Popup>
                            <b>{node.tags?.name || 'Sin nombre'}</b><br />
                            Amenity: {node.tags?.amenity || 'Desconocido'}
                        </Popup>
                    </Marker>
                ))
            }
        </>
    )
}
