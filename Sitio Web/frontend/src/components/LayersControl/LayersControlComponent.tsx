import * as turf from "@turf/turf";
import { LayerGroup, LayersControl, Marker, Polygon, Popup } from "react-leaflet";
import { useUserStore } from "../../state/State";
import comunasData from "./comunas.json";
import { MarcadorIcon } from "../MarcadorIcon/MarcadorIcon";

export const LayersControlComponent = () => {
    const { nodes, showMuseos, showMonumentos, showIglesias, showParques } = useUserStore();

    return (
        <LayersControl position="topright">
            {comunasData.features.map((feature: any, comunaIndex: any) => {
                // Crear el polígono usando las coordenadas de la comuna
                const polygonCoords = feature.geometry.coordinates.map((polygon: any) =>
                    polygon.map((coord: any) => [coord[1], coord[0]])
                );

                const turfPolygon = turf.polygon(polygonCoords);

                const pointsInPolygon = [
                    ...(showMuseos ? nodes.museos : []),
                    ...(showMonumentos ? nodes.monumentos : []),
                    ...(showIglesias ? nodes.iglesias : []),
                    ...(showParques ? nodes.parques : []),
                ].filter((point: any) => {
                    const turfPoint = turf.point([point.lat, point.lon]);
                    const isInPolygon = turf.booleanPointInPolygon(turfPoint, turfPolygon);
                    console.log(`Punto: [${point.lon}, ${point.lat}], En polígono: ${isInPolygon}`);
                    return isInPolygon;
                });
                

                const icon = MarcadorIcon({ color: "red" });

                return (
                    <LayersControl.Overlay key={comunaIndex} name={feature.properties.Comuna}>
                        <LayerGroup>
                            {/* Dibujar el perímetro de la comuna */}
                            {polygonCoords.map((polygon: any, polygonIndex: any) => (
                                <Polygon
                                    key={polygonIndex}
                                    positions={polygon}
                                    pathOptions={{ color: "blue" }}
                                >
                                    <Popup>
                                        <strong>{feature.properties.Comuna}</strong>
                                        <br />
                                        Región: {feature.properties.Region}
                                        <br />
                                        Provincia: {feature.properties.Provincia}
                                    </Popup>
                                </Polygon>
                            ))}

                            {pointsInPolygon.map((point, pointIndex) => (
                                
                                <Marker key={pointIndex} position={[point.lat, point.lon]} icon={icon}>
                                    <Popup>
                                        {point.type.charAt(0).toUpperCase() + point.type.slice(1)}
                                        dentro de {feature.properties.Comuna}
                                    </Popup>
                                </Marker>
                            ))}
                        </LayerGroup>
                    </LayersControl.Overlay>
                );
            })}
        </LayersControl>
    );
};
