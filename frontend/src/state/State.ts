import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

export interface UserSlice {
    showMuseos: boolean;
    showMonumentos: boolean;
    showIglesias: boolean;
    showParques: boolean;
    isModalOpen: boolean;
}

export interface UserActions {
    setShowMuseos: (state: boolean) => void;
    setShowMonumentos: (state: boolean) => void;
    setShowIglesias: (state: boolean) => void;
    setShowParques: (state: boolean) => void;
    openModal: () => void;
    closeModal: () => void;
}

export type UserState = UserSlice & UserActions;

export const useUserStore = create<UserState>()(
    immer<UserState>((set) => ({
        showMuseos: false,
        showMonumentos: false,
        showIglesias: false,
        showParques: false,
        isModalOpen: false,
        setShowMuseos: (showMuseos: boolean) => set({ showMuseos }),
        setShowMonumentos: (showMonumentos: boolean) => set({ showMonumentos }),
        setShowIglesias: (showIglesias: boolean) => set({ showIglesias }),
        setShowParques: (showParques: boolean) => set({ showParques }),
        openModal: () => set((state) => { state.isModalOpen = true; }),
        closeModal: () => set((state) => { state.isModalOpen = false; }),
    }))
);