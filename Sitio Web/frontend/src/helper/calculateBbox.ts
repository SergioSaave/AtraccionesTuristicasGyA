export const calculateBBox = (lat: number, lon: number, buffer: number) => {
    const south = lat - buffer;
    const north = lat + buffer;
    const west = lon - buffer;
    const east = lon + buffer;

    return [south, west, north, east];
};