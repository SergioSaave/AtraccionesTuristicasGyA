import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

export interface Node {
    type: string;
    id: number;
    lat: number;
    lon: number;
    tags: { [key: string]: string | undefined };
}

export interface UserSlice {
    showMuseos: boolean;
    showMonumentos: boolean;
    showIglesias: boolean;
    showParques: boolean;
    showAmenazas: boolean;
    isModalOpen: boolean;
    nodes: {
        museos: Node[];
        monumentos: Node[];
        iglesias: Node[];
        parques: Node[];
        amenazas: any[]; // Puedes especificar el tipo si es necesario
    };
}

export interface UserActions {
    setShowMuseos: (state: boolean) => void;
    setShowMonumentos: (state: boolean) => void;
    setShowIglesias: (state: boolean) => void;
    setShowParques: (state: boolean) => void;
    setShowAmenazas: (state: boolean) => void;
    openModal: () => void;
    closeModal: () => void;
    setNodes: (category: keyof UserSlice['nodes'], nodes: Node[]) => void;
}

export type UserState = UserSlice & UserActions;

export const useUserStore = create<UserState>()(
    immer<UserState>((set) => ({
        showMuseos: false,
        showMonumentos: false,
        showIglesias: false,
        showParques: false,
        showAmenazas: false,
        isModalOpen: false,
        nodes: {
            museos: [],
            monumentos: [],
            iglesias: [],
            parques: [],
            amenazas: [],
        },
        setShowMuseos: (showMuseos: boolean) => set({ showMuseos }),
        setShowMonumentos: (showMonumentos: boolean) => set({ showMonumentos }),
        setShowIglesias: (showIglesias: boolean) => set({ showIglesias }),
        setShowParques: (showParques: boolean) => set({ showParques }),
        setShowAmenazas: (showAmenazas: boolean) => set({ showAmenazas }),
        openModal: () => set((state) => { state.isModalOpen = true; }),
        closeModal: () => set((state) => { state.isModalOpen = false; }),
        setNodes: (category, nodes) =>
            set((state) => {
                state.nodes[category] = nodes;
            }),
    }))
);