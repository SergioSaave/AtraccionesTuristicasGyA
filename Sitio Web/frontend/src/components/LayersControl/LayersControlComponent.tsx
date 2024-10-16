import { Circle, FeatureGroup, LayerGroup, LayersControl, Marker, Popup, Rectangle } from "react-leaflet"

export const LayersControlComponent = () => {
    return (
        <LayersControl position="topright">
            <LayersControl.Overlay name="Marker with popup">
                <Marker position={[-33.447487, -70.673676]}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
            </LayersControl.Overlay>
            <LayersControl.Overlay checked name="Layer group with circles">
                <LayerGroup>
                    <Circle
                        center={[-33.447487, -70.673676]}
                        pathOptions={{ fillColor: 'blue' }}
                        radius={200}
                    />
                    <Circle
                        center={[-33.447487, -70.673676]}
                        pathOptions={{ fillColor: 'red' }}
                        radius={100}
                        stroke={false}
                    />
                    <LayerGroup>
                        <Circle
                            center={[51.51, -0.08]}
                            pathOptions={{ color: 'green', fillColor: 'green' }}
                            radius={100}
                        />
                    </LayerGroup>
                </LayerGroup>
            </LayersControl.Overlay>
            <LayersControl.Overlay name="Feature group">
                <FeatureGroup pathOptions={{ color: 'purple' }}>
                    <Popup>Popup in FeatureGroup</Popup>
                    <Circle center={[51.51, -0.06]} radius={200} />
                    <Rectangle bounds={[
                        [-33.447487, -70.6],
                        [-33.5, -70.673676],
                    ]} />
                </FeatureGroup>
            </LayersControl.Overlay>
        </LayersControl>
    )
}
