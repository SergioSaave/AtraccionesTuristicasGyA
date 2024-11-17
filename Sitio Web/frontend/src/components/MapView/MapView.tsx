import { Autocomplete, Box, Button, TextField } from '@mui/material'; // Importar Material UI components
import L from 'leaflet';
import { useEffect, useState } from 'react';
import { GeoJSON, MapContainer, Marker, Polyline, Popup, TileLayer, useMapEvents } from 'react-leaflet';
import { useUserStore } from '../../state/State';
import { LayersControlComponent } from '../LayersControl/LayersControlComponent';
import { Marcador } from '../Marcador/Marcador';
import { Suggestions } from './topSuggestions';

const center = [-33.447487, -70.673676]; // Santiago
const zoom = 12;

const routeCoordinates = [
    { lat: -33.4348395, lng: -70.6502397 },
    { lat: -33.4357267, lng: -70.6500681 },
    { lat: -33.4360475, lng: -70.6500287 },
    { lat: -33.4371844, lng: -70.6499091 },
    { lat: -33.4383452, lng: -70.6497052 },
    { lat: -33.4406451, lng: -70.649365 },
    { lat: -33.4412198, lng: -70.6492887 },
    { lat: -33.4418028, lng: -70.6492113 },
    { lat: -33.4433428, lng: -70.6489704 },
    { lat: -33.4434857, lng: -70.6495882 },
    { lat: -33.4440047, lng: -70.6521515 },
    { lat: -33.4441961, lng: -70.6529883 },
    { lat: -33.4444792, lng: -70.6542213 },
    { lat: -33.4446122, lng: -70.6548352 },
    { lat: -33.4447903, lng: -70.6556048 },
    { lat: -33.4451892, lng: -70.6573575 },
    { lat: -33.4454785, lng: -70.6586236 },
    { lat: -33.4458068, lng: -70.6600716 },
    { lat: -33.4459451, lng: -70.6606458 },
    { lat: -33.4459749, lng: -70.6607711 },
    { lat: -33.4468711, lng: -70.6645822 },
    { lat: -33.4469019, lng: -70.6647096 },
    { lat: -33.4476505, lng: -70.6674481 },
    { lat: -33.449856, lng: -70.6756376 },
    { lat: -33.4507192, lng: -70.678994 },
    { lat: -33.4507872, lng: -70.6792942 },
    { lat: -33.4514254, lng: -70.6808122 },
    { lat: -33.451823, lng: -70.6825512 },
    { lat: -33.4520285, lng: -70.683528 },
    { lat: -33.4523965, lng: -70.6851228 },
    { lat: -33.4530167, lng: -70.6877834 },
    { lat: -33.4533717, lng: -70.689293 },
    { lat: -33.4535992, lng: -70.6902573 },
    { lat: -33.4536918, lng: -70.6906533 },
    { lat: -33.453806, lng: -70.6911512 },
    { lat: -33.4540649, lng: -70.6922467 },
    { lat: -33.4542854, lng: -70.6921707 },
    { lat: -33.4548734, lng: -70.6919809 },
    { lat: -33.4585255, lng: -70.6907891 },
    { lat: -33.4589542, lng: -70.6919104 },
    { lat: -33.4592085, lng: -70.6925792 },
    { lat: -33.4597131, lng: -70.6940442 },
    { lat: -33.4599581, lng: -70.6946397 },
    { lat: -33.4602719, lng: -70.6952848 },
    { lat: -33.4605879, lng: -70.6959884 },
    { lat: -33.461798, lng: -70.6985041 },
    { lat: -33.4642997, lng: -70.7045008 },
    { lat: -33.4644673, lng: -70.7049895 },
    { lat: -33.464493, lng: -70.7050631 },
    { lat: -33.4645055, lng: -70.7050968 },
    { lat: -33.4645289, lng: -70.7051625 },
    { lat: -33.4670938, lng: -70.7109328 },
    { lat: -33.4671581, lng: -70.7110733 },
    { lat: -33.4696849, lng: -70.7165442 },
    { lat: -33.4712939, lng: -70.7192524 },
    { lat: -33.4715827, lng: -70.719717 },
    { lat: -33.4717368, lng: -70.7199487 },
    { lat: -33.4719347, lng: -70.720259 },
    { lat: -33.4725013, lng: -70.7211367 },
    { lat: -33.47302, lng: -70.7218831 },
    { lat: -33.4731237, lng: -70.7219942 },
    { lat: -33.4732221, lng: -70.7220854 },
    { lat: -33.4733357, lng: -70.7221964 },
    { lat: -33.4733333, lng: -70.7223959 },
    { lat: -33.4734478, lng: -70.7225839 },
    { lat: -33.4737834, lng: -70.7229635 },
    { lat: -33.4790802, lng: -70.7310795 },
    { lat: -33.4792917, lng: -70.7315251 },
    { lat: -33.4821509, lng: -70.7374813 },
    { lat: -33.4824266, lng: -70.7381706 },
    { lat: -33.4824818, lng: -70.7383117 },
    { lat: -33.4825782, lng: -70.7382226 },
    { lat: -33.4829266, lng: -70.7379319 },
    { lat: -33.4833628, lng: -70.7377425 },
    { lat: -33.4834901, lng: -70.7377455 },
    { lat: -33.4835776, lng: -70.7377636 },
    { lat: -33.4839501, lng: -70.7378668 },
    { lat: -33.4841581, lng: -70.7378773 },
    { lat: -33.4845824, lng: -70.7378514 }
];


interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: { [key: string]: string | undefined };
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
            console.log(e.latlng);
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
    const [address, setAddress] = useState<string>(''); // Dirección ingresada
    const [position, setPosition] = useState<L.LatLng | null>(null); // Para manejar la ubicación actual

    const [nodesMuseos, setNodesMuseos] = useState<Node[]>([]);
    const [nodesMonumentos, setNodesMonumentos] = useState<Node[]>([]);
    const [nodesIglesias, setNodesIglesias] = useState<Node[]>([]);
    const [nodesAmenazas, setNodesAmenazas] = useState<any>([]);

    const showMuseos = useUserStore((state) => state.showMuseos);
    const showMonumentos = useUserStore((state) => state.showMonumentos);
    const showIglesias = useUserStore((state) => state.showIglesias);
    const showAmenazas = useUserStore((state) => state.showAmenazas);
    const showParques = useUserStore((state) => state.showParques);

    const openModal = useUserStore((state) => state.openModal);

    const setNodes = useUserStore((state) => state.setNodes);

    const getMuseos = async () => {
        const response = await fetch('http://127.0.0.1:5000/museos');
        const data = await response.json();
        console.log(data);
        const nodesData = data.elements.filter((element: { type: string; }) => element.type === 'node') as Node[];
        setNodes('museos', nodesData);
        setNodesMuseos(nodesData);
    }

    // Función para manejar el cambio de la dirección
    const handleAddressChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setAddress(event.target.value);
    };

    // Función para usar la ubicación actual
    const handleUseCurrentLocation = () => {
        if (position) {
            map?.flyTo(position, 14); // Vuela a la posición actual
        }
    };

    useEffect(() => {
        getMuseos();
    }, []);

    return (
        <>
            <Box
                sx={{
                    position: 'absolute',
                    top: 10,
                    left: 10,
                    zIndex: 1000,
                    backgroundColor: 'white',
                    padding: '10px',
                    borderRadius: '5px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.15)',
                    width: '350px',
                }}
            >
                <Autocomplete
                    multiple
                    options={Suggestions}
                    getOptionLabel={(option) => option.title}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            variant="outlined"
                            label="Selecciona los lugares!"
                        />
                    )}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleUseCurrentLocation}
                    fullWidth
                    sx={{ marginY: '5px' }}
                >
                    Usar mi direccion
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={openModal}
                    fullWidth
                >
                    Abrir Modal
                </Button>
            </Box>
            <MapContainer
                center={[center[0], center[1]]}
                zoomControl={false}
                zoom={zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
                ref={setMap}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[-33.6112285, -70.626491]}>
                </Marker>
                <Polyline positions={routeCoordinates} color="blue" weight={4} />
                {
                    showMuseos ? <Marcador nodes={nodesMuseos} color={'blue'} /> : null
                }
                <LayersControlComponent />
                <LocationMarker />
            </MapContainer>
        </>
    );
};
