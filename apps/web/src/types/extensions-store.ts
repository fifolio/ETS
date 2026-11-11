import type { InstalledExtension } from "./extension";

export interface ExtensionsState {
    items: InstalledExtension[];
    loaded: boolean;
    error: string;
}

export interface ExtensionsActions {
    load: () => Promise<void>;
    remove: (id: string) => Promise<void>;
    clear: () => void;
}

export type ExtensionsStore = ExtensionsState & ExtensionsActions;