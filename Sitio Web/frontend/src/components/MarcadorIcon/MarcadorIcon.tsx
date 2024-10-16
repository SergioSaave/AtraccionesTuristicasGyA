import L from "leaflet";

interface MarkerIconProps {
    color: string;
}

export const MarcadorIcon = ({ color }: MarkerIconProps) => {
    // URL de los íconos con el color deseado
    const iconUrl = `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`;

    return new L.Icon({
        iconUrl: iconUrl,
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
    });
};
