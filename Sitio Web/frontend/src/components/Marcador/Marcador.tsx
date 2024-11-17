import { Marker, Popup } from "react-leaflet";
import { MarcadorIcon } from "../MarcadorIcon/MarcadorIcon";

interface Node {
    id: number;
    lat: number;
    lon: number;
    tags: { [key: string]: string | undefined };
}

interface MarcadorProps {
    nodes: any;
    // getColor: (tags: { [key: string]: string | undefined }) => string;
    color: string;
}

export const Marcador = ({ nodes, color }: MarcadorProps) => {
    return (
        <>
            {nodes.map((node: any) => {
                // const color = getColor(node.tags);
                const icon = MarcadorIcon({ color });

                return (
                    <Marker key={node.id} position={[node.lat, node.lon]} icon={icon}>
                        <Popup>
                            <b>{node.tags?.name || 'Sin nombre'}</b><br />
                            Amenity: {node.tags?.description || 'Desconocido'}
                        </Popup>
                    </Marker>
                );
            })}
        </>
    );
};
