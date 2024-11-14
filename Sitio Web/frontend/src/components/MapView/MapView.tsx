import L from 'leaflet';
import { useCallback, useEffect, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer, useMapEvents } from 'react-leaflet';
import { Marcador } from '../Marcador/Marcador';
import { calculateBBox } from '../../helper/calculateBbox';
import { useUserStore } from '../../state/State';
import { LayersControlComponent } from '../LayersControl/LayersControlComponent';
import { Circulos } from '../Circulos/Circulos';

const center = [-33.447487, -70.673676]; // Santiago
const zoom = 12;

interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: { [key: string]: string | undefined };
}

function DisplayPosition({ map }: any) {
    const [position, setPosition] = useState(() => map.getCenter());

    const onClick = useCallback(() => {
        map.setView(center, zoom);
    }, [map]);

    const onMove = useCallback(() => {
        const { lat, lng } = map.getCenter();
        console.log(calculateBBox(lat, lng, 0.01));

        setPosition(map.getCenter());
    }, [map]);

    useEffect(() => {
        map.on('move', onMove);
        return () => {
            map.off('move', onMove);
        };
    }, [map, onMove]);

    useEffect(() => {
        const { lat, lng } = map.getCenter();
        console.log(calculateBBox(lat, lng, 0.01));
    }, [])

    return (
        <p>
            latitude: {position.lat.toFixed(4)}, longitude: {position.lng.toFixed(4)}{' '}
            <button onClick={onClick}>reset</button>
        </p>
    );
}

function LocationMarker() {
    const [position, setPosition] = useState<L.LatLng | null>(null);
    const [hasFlown, setHasFlown] = useState(false); // Nuevo estado para controlar el vuelo inicial

    const map = useMapEvents({
        click() {
            // Solo localiza y vuela si no se ha hecho antes
            if (!hasFlown) {
                map.locate();
            }
        },
        locationfound(e) {
            setPosition(e.latlng);
            if (!hasFlown) {
                map.flyTo(e.latlng, map.getZoom());
                setHasFlown(true); // Marca que el vuelo inicial ya ocurrió
            }
        },
    });

    return position === null ? null : (
        <Marker position={position}>
            <Popup>You are here</Popup>
        </Marker>
    );
}

export const MapView = () => {
    const [map, setMap] = useState<L.Map | null>(null);
    const [nodesMuseos, setNodesMuseos] = useState<Node[]>([]);
    const [nodesMonumentos, setNodesMonumentos] = useState<Node[]>([]);
    const [nodesIglesias, setNodesIglesias] = useState<Node[]>([]);
    const [nodesAmenazas, setNodesAmenazas] = useState<any>([]);
    const [nodesParques, setNodesParques] = useState<Node[]>([]);

    const showMuseos = useUserStore((state) => state.showMuseos);
    const showMonumentos = useUserStore((state) => state.showMonumentos);
    const showIglesias = useUserStore((state) => state.showIglesias);
    const showAmenazas = useUserStore((state) => state.showAmenazas);
    const showParques = useUserStore((state) => state.showParques);

    const setNodes = useUserStore((state) => state.setNodes);

    const getMuseos = async () => {
        const response = await fetch('http://127.0.0.1:5000/museos');
        const data = await response.json();
        console.log(data);
        const nodesData = data.elements.filter((element: { type: string; }) => element.type === 'node') as Node[];
        setNodesMuseos(nodesData);
        setNodes('museos', nodesData);
    }

    const getMonumentos = async () => {
        const response = await fetch('http://127.0.0.1:5000/monumentos');
        const data = await response.json();
        console.log(data);
        const nodesData = data.elements.filter((element: { type: string; }) => element.type === 'node') as Node[];
        setNodesMonumentos(nodesData);
        setNodes('monumentos', nodesData);
    }

    const getIglesias = async () => {
        const response = await fetch('http://127.0.0.1:5000/iglesias');
        const data = await response.json();
        console.log(data);
        const nodesData = data.elements.filter((element: { type: string; }) => element.type === 'node') as Node[];
        setNodesIglesias(nodesData);
        setNodes('iglesias', nodesData);
    }

    const getParques = async () => {
        const response = await fetch('http://127.0.0.1:5000/parques');
        const data = await response.json();
        console.log(data);
        const nodesData = data.elements.filter((element: { type: string; }) => element.type === 'node') as Node[];
        setNodesParques(nodesData);
        setNodes('parques', nodesData);
    }

    const getAmenazas = async () => {
        const response = await fetch('http://127.0.0.1:5000/api/hexagons');
        const data = await response.json();
        console.log(data);
        setNodesAmenazas(data);
        setNodes('amenazas', data);
    }

    useEffect(() => {
        getMuseos();
        getMonumentos();
        getIglesias();
        getParques();
        getAmenazas();
    }, []);

    // Función para determinar el color según el tipo de lugar
    // const getColor = (tags: { [key: string]: string | undefined }) => {
    //     if (tags.amenity === 'cafe') {
    //         return 'red';
    //     } else if (tags.amenity === 'park') {
    //         return 'green';
    //     } else if (tags.tourism === 'museum') {
    //         return 'orange';
    //     }
    //     return 'blue';
    // };

    return (
        <>
            {map ? <DisplayPosition map={map} /> : null}

            <MapContainer
                center={[center[0], center[1]]}
                zoom={zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
                ref={setMap}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {
                    showMuseos ? <Marcador nodes={nodesMuseos} color={'blue'} /> : null
                }
                {
                    showMonumentos ? <Marcador nodes={nodesMonumentos} color={'yellow'} /> : null
                }
                {
                    showIglesias ? <Marcador nodes={nodesIglesias} color={'grey'} /> : null
                }
                {
                    showParques ? <Marcador nodes={nodesParques} color={'green'} /> : null
                }
                {
                    showAmenazas ? <Circulos coordinates={nodesAmenazas} color={'red'} radius={300} /> : null
                }
                <LayersControlComponent />
                <LocationMarker />
            </MapContainer>
        </>
    );
};
