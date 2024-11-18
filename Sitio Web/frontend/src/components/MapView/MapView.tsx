import { Autocomplete, Box, Button, TextField } from '@mui/material'; // Importar Material UI components
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMapEvents } from 'react-leaflet';
import { useUserStore } from '../../state/State';
import { LayersControlComponent } from '../LayersControl/LayersControlComponent';
import { Marcador } from '../Marcador/Marcador';
import { Suggestions } from './topSuggestions';
import { toast } from 'sonner';
import { Circulos } from '../Circulos/Circulos';

const center = [-33.447487, -70.673676]; // Santiago
const zoom = 12;

const routeCoordinateas = [
    { lat: -33.3863141, lng: -70.562683 },
    { lat: -33.3860916, lng: -70.5625951 },
    { lat: -33.3860399, lng: -70.5620878 },
    { lat: -33.3860055, lng: -70.5616798 },
    { lat: -33.3854959, lng: -70.5568314 },
    { lat: -33.3854671, lng: -70.5562068 },
    { lat: -33.3853357, lng: -70.5556891 },
    { lat: -33.3850597, lng: -70.5546723 },
    { lat: -33.3847451, lng: -70.553726 },
    { lat: -33.3845559, lng: -70.5532163 },
    { lat: -33.3839738, lng: -70.551655 },
    { lat: -33.3838749, lng: -70.5513898 },
    { lat: -33.3837931, lng: -70.5511705 },
    { lat: -33.3839145, lng: -70.5511109 },
    { lat: -33.3858492, lng: -70.5501684 },
    { lat: -33.3862836, lng: -70.5499539 },
    { lat: -33.3876879, lng: -70.549297 },
    { lat: -33.3895945, lng: -70.5485049 },
    { lat: -33.3896269, lng: -70.5485858 },
    { lat: -33.3897009, lng: -70.5487778 },
    { lat: -33.3899886, lng: -70.5495525 },
    { lat: -33.3915648, lng: -70.5536049 },
    { lat: -33.3930584, lng: -70.5579684 },
    { lat: -33.3943528, lng: -70.5617607 },
    { lat: -33.3951502, lng: -70.5640687 },
    { lat: -33.3953771, lng: -70.5647093 },
    { lat: -33.3962257, lng: -70.5669545 },
    { lat: -33.3968917, lng: -70.5689031 },
    { lat: -33.3971364, lng: -70.5695821 },
    { lat: -33.3973038, lng: -70.5700803 },
    { lat: -33.3974632, lng: -70.570617 },
    { lat: -33.3976331, lng: -70.5710752 },
    { lat: -33.3977744, lng: -70.5714445 },
    { lat: -33.3978685, lng: -70.5716792 },
    { lat: -33.3981199, lng: -70.5722237 },
    { lat: -33.398528, lng: -70.5732965 },
    { lat: -33.3995324, lng: -70.5759724 },
    { lat: -33.3996353, lng: -70.5762309 },
    { lat: -33.4013688, lng: -70.5804118 },
    { lat: -33.4031576, lng: -70.5846765 },
    { lat: -33.403233, lng: -70.5848434 },
    { lat: -33.4037297, lng: -70.5855475 },
    { lat: -33.4038159, lng: -70.5857259 },
    { lat: -33.4040919, lng: -70.5866638 },
    { lat: -33.4045652, lng: -70.5889558 },
    { lat: -33.4052959, lng: -70.5913941 },
    { lat: -33.4077747, lng: -70.6001601 },
    { lat: -33.4077217, lng: -70.6004236 },
    { lat: -33.4078759, lng: -70.6006068 },
    { lat: -33.4079675, lng: -70.6007114 },
    { lat: -33.4084517, lng: -70.6011802 },
    { lat: -33.4085224, lng: -70.6012445 },
    { lat: -33.408837, lng: -70.601561 },
    { lat: -33.409268, lng: -70.6020103 },
    { lat: -33.4098759, lng: -70.602255 },
    { lat: -33.4105392, lng: -70.6024991 },
    { lat: -33.4107681, lng: -70.6025789 },
    { lat: -33.411296, lng: -70.6027398 },
    { lat: -33.4115547, lng: -70.6027916 },
    { lat: -33.4137548, lng: -70.6035351 },
    { lat: -33.4138942, lng: -70.603576 },
    { lat: -33.4146356, lng: -70.6038299 },
    { lat: -33.416053, lng: -70.6043156 },
    { lat: -33.416968, lng: -70.6048397 },
    { lat: -33.4170315, lng: -70.6048774 },
    { lat: -33.4172489, lng: -70.6049937 },
    { lat: -33.4173444, lng: -70.605038 },
    { lat: -33.4179586, lng: -70.6052974 },
    { lat: -33.4197736, lng: -70.6060353 },
    { lat: -33.4207662, lng: -70.6080912 },
    { lat: -33.4217846, lng: -70.6098597 },
    { lat: -33.4223545, lng: -70.6107301 },
    { lat: -33.4235813, lng: -70.6124488 },
    { lat: -33.4256123, lng: -70.6147092 },
    { lat: -33.4275699, lng: -70.6173632 },
    { lat: -33.4288335, lng: -70.6203284 },
    { lat: -33.4299271, lng: -70.6222263 },
    { lat: -33.4310057, lng: -70.6236818 },
    { lat: -33.4311687, lng: -70.623876 },
    { lat: -33.4314906, lng: -70.6242545 },
    { lat: -33.4323988, lng: -70.6253157 },
    { lat: -33.4337933, lng: -70.6268214 },
    { lat: -33.434844, lng: -70.6283546 },
    { lat: -33.4353244, lng: -70.6294345 },
    { lat: -33.4355627, lng: -70.6299857 },
    { lat: -33.4366338, lng: -70.634278 },
    { lat: -33.436645, lng: -70.634524 },
    { lat: -33.4367659, lng: -70.6347584 },
    { lat: -33.4372672, lng: -70.6346086 },
    { lat: -33.4372134, lng: -70.6342151 },
    { lat: -33.4440765, lng: -70.6317814 },
    { lat: -33.444364, lng: -70.631419 },
    { lat: -33.4450886, lng: -70.6310939 },
    { lat: -33.4471562, lng: -70.6305325 },
    { lat: -33.4523265, lng: -70.6291461 },
    { lat: -33.4524527, lng: -70.6291129 },
    { lat: -33.454477, lng: -70.6285637 },
    { lat: -33.4547715, lng: -70.6284832 },
    { lat: -33.455112, lng: -70.6283921 },
    { lat: -33.4553935, lng: -70.6297827 },
    { lat: -33.45542, lng: -70.6299213 },
    { lat: -33.4555892, lng: -70.6299184 },
    { lat: -33.4648451, lng: -70.627247 },
    { lat: -33.4658253, lng: -70.6269674 },
    { lat: -33.4673987, lng: -70.6265169 },
    { lat: -33.4711561, lng: -70.6241452 },
    { lat: -33.4718288, lng: -70.6239527 },
    { lat: -33.4749246, lng: -70.6231433 },
    { lat: -33.474923, lng: -70.6230343 },
    { lat: -33.4749197, lng: -70.6228973 },
    { lat: -33.4720811, lng: -70.6236188 },
    { lat: -33.4712877, lng: -70.6225712 },
    { lat: -33.4711275, lng: -70.6215242 },
    { lat: -33.4710524, lng: -70.6210908 },
    { lat: -33.4708212, lng: -70.617151 },
    { lat: -33.470794, lng: -70.6166086 }
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
    const [nodesMonumentos, setNodesMonumentos] = useState<Node[]>([]);
    const [nodesIglesias, setNodesIglesias] = useState<Node[]>([]);
    const [nodesParques, setNodesParques] = useState<Node[]>([]);
    const [nodesAmenazas, setNodesAmenazas] = useState<any>([]);
    const [selectedOptions, setSelectedOptions] = useState<any[]>([]);
    const [routeCoordinates, setRouteCoordinates] = useState<[number, number][]>([]); // Coordenadas de la ruta

    const showMuseos = useUserStore((state) => state.showMuseos);
    const showMonumentos = useUserStore((state) => state.showMonumentos);
    const showIglesias = useUserStore((state) => state.showIglesias);
    const showParques = useUserStore((state) => state.showParques);
    const showAmenazas = useUserStore((state) => state.showAmenazas);
    const setNodes = useUserStore((state) => state.setNodes);
    const openModal = useUserStore((state) => state.openModal);

    const getMuseos = async () => {
        const response = await fetch('http://127.0.0.1:5000/museos');
        const data = await response.json();
        const nodesData = data.elements.filter((element: { type: string }) => element.type === 'node') as Node[];
        setNodes('museos', nodesData);
        setNodesMuseos(nodesData);
    };

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
        getMonumentos();
        getIglesias();
        getParques();
        getAmenazas();
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
                <Polyline positions={routeCoordinateas} />
                {routeCoordinates.length > 0 && (
                    <Polyline
                        positions={routeCoordinates}
                        color="blue"
                        weight={4}
                        opacity={0.8}
                    />
                )}
                {showMuseos && <Marcador nodes={nodesMuseos} color={'blue'} />}
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
