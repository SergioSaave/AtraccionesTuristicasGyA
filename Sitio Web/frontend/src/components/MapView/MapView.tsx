import { Autocomplete, Box, Button, TextField } from '@mui/material'; // Importar Material UI components
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMapEvents } from 'react-leaflet';
import { useUserStore } from '../../state/State';
import { LayersControlComponent } from '../LayersControl/LayersControlComponent';
import { Marcador } from '../Marcador/Marcador';
import { Suggestions } from './topSuggestions';
import { toast } from 'sonner';

const center = [-33.447487, -70.673676]; // Santiago
const zoom = 12;

interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: { [key: string]: string | undefined };
}

function LocationMarker() {
    const [position, setPosition] = useState<L.LatLng | null>(null);
    const [hasFlown, setHasFlown] = useState(false); // Estado para controlar el vuelo inicial

    const map = useMapEvents({
        click() {
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
    const [address, setAddress] = useState<string>(''); // Dirección ingresada
    const [position, setPosition] = useState<L.LatLng | null>(null); // Para manejar la ubicación actual
    const [nodesMuseos, setNodesMuseos] = useState<Node[]>([]);
    const [selectedOptions, setSelectedOptions] = useState<any[]>([]);
    const [routeCoordinates, setRouteCoordinates] = useState<[number, number][]>([]); // Coordenadas de la ruta

    const showMuseos = useUserStore((state) => state.showMuseos);
    const setNodes = useUserStore((state) => state.setNodes);
    const openModal = useUserStore((state) => state.openModal);

    const getMuseos = async () => {
        const response = await fetch('http://127.0.0.1:5000/museos');
        const data = await response.json();
        const nodesData = data.elements.filter((element: { type: string }) => element.type === 'node') as Node[];
        setNodes('museos', nodesData);
        setNodesMuseos(nodesData);
    };

    const handleCreateRoute = async () => {
        if (selectedOptions.length < 2) {
            toast.error('Selecciona al menos dos opciones antes de crear la ruta.');
            return;
        }

        toast.loading('Creando ruta...');
        try {
            const response = await fetch(
                `http://127.0.0.1:5000/consultar-datos?lat_inicio=${selectedOptions[0].lat}&lon_inicio=${selectedOptions[0].lon}&lat_fin=${selectedOptions[1].lat}&lon_fin=${selectedOptions[1].lon}`
            );

            // Verifica si la respuesta fue exitosa
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error en la respuesta de la API:', errorText);
                toast.error('Error al comunicarse con el servidor.');
                return;
            }

            const data: { lat: number; lng: number }[] = await response.json();

            // Log para depuración
            console.log('Respuesta de la API:', data);

            if (data && data.length > 0) {
                const coordinates = data.map((point) => [point.lat, point.lng] as [number, number]); // Convertir al formato [[lat, lng], ...]
                setRouteCoordinates(coordinates);
                toast.success('Ruta creada exitosamente.');
                map?.fitBounds(coordinates); // Ajustar el mapa a las coordenadas de la ruta
            } else {
                console.error('Respuesta inesperada de la API:', data);
                toast.error('No se pudo crear la ruta.');
            }
        } catch (error) {
            console.error('Error al crear la ruta:', error);
            toast.error('Error al crear la ruta.');
        }
    };



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
                    value={selectedOptions}
                    onChange={(event, newValue) => setSelectedOptions(newValue)}
                    renderInput={(params) => (
                        <TextField {...params} variant="outlined" label="Selecciona los lugares!" />
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
                    onClick={handleCreateRoute}
                    fullWidth
                    sx={{ marginY: '5px' }}
                >
                    Crear Ruta!
                </Button>
                <Button variant="contained" color="primary" onClick={openModal} fullWidth>
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
                {routeCoordinates.length > 0 && (
                    <Polyline
                        positions={routeCoordinates}
                        color="blue"
                        weight={4}
                        opacity={0.8}
                    />
                )}
                {showMuseos && <Marcador nodes={nodesMuseos} color={'blue'} />}
                <LayersControlComponent />
                <LocationMarker />
            </MapContainer>
        </>
    );
};
