export interface Overpass {
    version: number;
    generator: string;
    osm3s: Osm3S;
    elements: Element[];
}

export interface Element {
    type: Type;
    id: number;
    lat?: number;
    lon?: number;
    tags: { [key: string]: string };
    bounds?: Bounds;
    nodes?: number[];
    geometry?: Geometry[];
    members?: Member[];
}

export interface Bounds {
    minlat: number;
    minlon: number;
    maxlat: number;
    maxlon: number;
}

export interface Geometry {
    lat: number;
    lon: number;
}

export interface Member {
    type: Type;
    ref: number;
    role: Role;
    geometry: Geometry[];
}

export enum Role {
    Inner = "inner",
    Outer = "outer",
}

export enum Type {
    Node = "node",
    Relation = "relation",
    Way = "way",
}

export interface Osm3S {
    copyright: string;
}
