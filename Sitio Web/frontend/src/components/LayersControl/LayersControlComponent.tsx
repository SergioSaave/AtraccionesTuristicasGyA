import * as turf from "@turf/turf";
import { LayerGroup, LayersControl, Marker, Polygon, Popup, GeoJSON } from "react-leaflet";
import { useEffect, useState } from "react";
import { useUserStore } from "../../state/State";
import comunasData from "./comunas.json";
import { MarcadorIcon } from "../MarcadorIcon/MarcadorIcon";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from "@mui/material";
import { toast } from 'sonner';

export const LayersControlComponent = () => {

    const [geojsonData, setGeojsonData] = useState(null);

    useEffect(() => {
        fetch('/comunas_afectadas.geojson')
            .then((response) => response.json())
            .then((data) => setGeojsonData(data));
    }, []);

    const getColor = (percentage: any) => {
        // Convertir porcentaje a número y decidir el color
        const percent = parseFloat(percentage);
        return percent > 3 ? 'red' : 'blue';
    };

    const style = (feature: any) => {
        const percentage = feature.properties.PORCENTAJE; // Eliminar espacios en blanco
        return {
            fillColor: getColor(percentage),
            weight: 2,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.3,
        };
    };

    const { nodes, showMuseos, showMonumentos, showIglesias, showParques } = useUserStore();
    const [openDialog, setOpenDialog] = useState(false);
    const [dialogContent, setDialogContent] = useState({ title: "", description: "" });

    const fetchMuseoData = async (nombreMuseo: any) => {
        const loadingToast = toast("Cargando...", { duration: Infinity });

        try {
            const response = await fetch(`http://127.0.0.1:5000/buscar-museo?nombre_museo=${encodeURIComponent(nombreMuseo)}`);
            const data = await response.json();

            // Asignamos los datos recibidos al contenido del diálogo
            setDialogContent({
                title: data.nombre || nombreMuseo,
                description: data.descripcion || "Información no disponible",
            });
        } catch (error) {
            console.error("Error al buscar la información del museo:", error);
            setDialogContent({
                title: nombreMuseo,
                description: "Error al cargar la información del museo.",
            });
        } finally {
            toast.dismiss(loadingToast);  // Cerrar el toast de "Cargando..."
            setOpenDialog(true);          // Abrir el modal con la información
        }
    };

    const handleOpenDialog = (nombreMuseo: any) => {
        fetchMuseoData(nombreMuseo);
    };

    return (
        <>
            <LayersControl position="topright">
                <LayersControl.Overlay name="Mostrar amenaza ENEL">
                    <LayerGroup>
                        {geojsonData &&
                            <GeoJSON data={geojsonData} style={style} />
                        }
                    </LayerGroup>
                </LayersControl.Overlay>
                <LayersControl.Overlay name="Mostrar amenaza STOP">
                    <LayerGroup>
                        {geojsonData &&
                            <GeoJSON data={geojsonData} style={style} />
                        }
                    </LayerGroup>
                </LayersControl.Overlay>
                {comunasData.features.map((feature, comunaIndex) => {
                    const polygonCoords = feature.geometry.coordinates.map((polygon) =>
                        polygon.map((coord) => [coord[1], coord[0]])
                    );

                    const turfPolygon = turf.polygon(polygonCoords);

                    const pointsInPolygon = [
                        ...(showMuseos ? nodes.museos : []),
                        ...(showMonumentos ? nodes.monumentos : []),
                        ...(showIglesias ? nodes.iglesias : []),
                        ...(showParques ? nodes.parques : []),
                    ].filter((point) => {
                        const turfPoint = turf.point([point.lat, point.lon]);
                        const isInPolygon = turf.booleanPointInPolygon(turfPoint, turfPolygon);
                        return isInPolygon;
                    });

                    const icon = MarcadorIcon({ color: "red" });

                    return (
                        <LayersControl.Overlay key={comunaIndex} name={feature.properties.Comuna}>
                            <LayerGroup>
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
                                            {point.tags?.name || "Sin nombre"}
                                            <br />
                                            <Button
                                                variant="text"
                                                color="primary"
                                                onClick={() => handleOpenDialog(point.tags?.name || "Sin nombre")}
                                            >
                                                Ver más
                                            </Button>
                                        </Popup>
                                    </Marker>
                                ))}
                            </LayerGroup>
                        </LayersControl.Overlay>
                    );
                })}
            </LayersControl>

            {/* Dialog para mostrar información del museo */}
            <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
                <DialogTitle>{dialogContent.title}</DialogTitle>
                <DialogContent>
                    <Typography>{dialogContent.description}</Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDialog(false)} color="primary">
                        Cerrar
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};
