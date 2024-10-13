import L from 'leaflet';
import { useCallback, useEffect, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { Marcador } from '../Marcador/Marcador';
import { calculateBBox } from '../../helper/calculateBbox';

const center = [-33.447487, -70.673676] // Santiago
const zoom = 12;
// const zoom = 18;

function DisplayPosition({ map }: any) {
    const [position, setPosition] = useState(() => map.getCenter())

    const onClick = useCallback(() => {
        map.setView(center, zoom)
    }, [map])

    const onMove = useCallback(() => {
        // console.log(map.getCenter().lat)
        // console.log(map.getCenter().lng)
        const { lat, lng } = map.getCenter();
        console.log(calculateBBox(lat, lng, 0.01))

        setPosition(map.getCenter())
    }, [map])

    useEffect(() => {
        map.on('move', onMove)
        return () => {
            map.off('move', onMove)
        }
    }, [map, onMove])

    return (
        <p>
            latitude: {position.lat.toFixed(4)}, longitude: {position.lng.toFixed(4)}{' '}
            <button onClick={onClick}>reset</button>
        </p>
    )
}

export const MapView = () => {
    const [map, setMap] = useState<L.Map | null>(null);

    return (
        <>
            {map ? <DisplayPosition map={map} /> : null}

            <MapContainer
                center={[-33.447487, -70.673676]}
                zoom={zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
                ref={setMap}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marcador />
            </MapContainer>
        </>
    );
};
