import { create } from "zustand";

import { getExtensions } from "@/services/extensions/get-extensions";
import { removeExtension } from "@/services/extensions/remove-extension";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";
import type { ExtensionsStore } from "@/types/extension/extensions-store";

export const useExtensionsStore = create<ExtensionsStore>()((set, get) => ({
    items: [],
    loaded: false,
    error: "",

    load: async () => {
        try {
            set({ items: await getExtensions(), loaded: true, error: "" });
        } catch (err) {
            set({
                loaded: true,
                error: err instanceof Error ? err.message : "Could not load your extensions.",
            });
        }
    },
    remove: async (id) => {
        await removeExtension(id);
        await get().load();
        // Removing the last extension makes the setup incomplete again.
        await useOnboardingStore.getState().load();
    },
    clear: () => set({ items: [], loaded: false, error: "" }),
}));