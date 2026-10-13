import { create } from "zustand";
import type { CollectionRecord } from "../types";

interface AppState {
  selectedCollectionId: string | null;
  sidebarCollapsed: boolean;
  collections: CollectionRecord[];
  setSelectedCollectionId: (id: string | null) => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;
  setCollections: (collections: CollectionRecord[]) => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedCollectionId: null,
  sidebarCollapsed: false,
  collections: [],

  setSelectedCollectionId: (id) =>
    set({ selectedCollectionId: id }),

  setSidebarCollapsed: (collapsed) =>
    set({ sidebarCollapsed: collapsed }),

  toggleSidebar: () =>
    set((state) => ({
      sidebarCollapsed: !state.sidebarCollapsed,
    })),

  setCollections: (collections) =>
    set({ collections }),
}));