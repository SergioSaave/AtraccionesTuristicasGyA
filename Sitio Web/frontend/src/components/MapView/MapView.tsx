import L from 'leaflet';
import { useCallback, useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMapEvents } from 'react-leaflet';
import { Marcador } from '../Marcador/Marcador';
import { calculateBBox } from '../../helper/calculateBbox';
import { useUserStore } from '../../state/State';
import { LayersControlComponent } from '../LayersControl/LayersControlComponent';
import { Circulos } from '../Circulos/Circulos';

const center = [-33.447487, -70.673676]; // Santiago
const zoom = 12;

const routeCoordinates = [
    { lat: -33.4369052, lng: -70.6368676 },
    { lat: -33.4374994, lng: -70.6365692 },
    { lat: -33.4376332, lng: -70.6364854 },
    { lat: -33.4372991, lng: -70.6352693 },
    { lat: -33.4372689, lng: -70.6351382 },
    { lat: -33.4370971, lng: -70.6352106 },
    { lat: -33.4368263, lng: -70.635324 },
    { lat: -33.4363944, lng: -70.6354179 },
    { lat: -33.4360606, lng: -70.6369504 },
    { lat: -33.4355916, lng: -70.6389665 },
    { lat: -33.4346947, lng: -70.6428396 },
    { lat: -33.4346185, lng: -70.6431936 },
    { lat: -33.4340793, lng: -70.6454862 },
    { lat: -33.4334748, lng: -70.6480418 },
    { lat: -33.4332674, lng: -70.648782 },
    { lat: -33.4330994, lng: -70.6494706 },
    { lat: -33.4328733, lng: -70.6504441 },
    { lat: -33.4327178, lng: -70.6511349 },
    { lat: -33.4326569, lng: -70.6517216 },
    { lat: -33.4324156, lng: -70.6516803 },
    { lat: -33.432392, lng: -70.6516763 },
    { lat: -33.4320136, lng: -70.6515999 },
    { lat: -33.4319521, lng: -70.6515982 },
    { lat: -33.4316775, lng: -70.6516398 },
    { lat: -33.4311646, lng: -70.651728 },
    { lat: -33.4249469, lng: -70.6511993 },
    { lat: -33.42511, lng: -70.6533697 },
    { lat: -33.4252507, lng: -70.6546553 },
    { lat: -33.4207593, lng: -70.6556612 },
    { lat: -33.4206014, lng: -70.655695 },
    { lat: -33.4176521, lng: -70.6563592 },
    { lat: -33.4155969, lng: -70.657143 },
    { lat: -33.4156069, lng: -70.6573704 },
    { lat: -33.4155991, lng: -70.6642851 },
    { lat: -33.4148827, lng: -70.6646023 },
    { lat: -33.4137063, lng: -70.6650593 },
    { lat: -33.4135588, lng: -70.6632573 }
];

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
                <Polyline positions={routeCoordinates} color="blue" weight={4} />
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
