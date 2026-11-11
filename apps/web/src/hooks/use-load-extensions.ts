import { useEffect } from "react";

import { useExtensionsStore } from "@/stores/extension/extensions-store";

export function useLoadExtensions() {
    const loaded = useExtensionsStore((state) => state.loaded);
    const error = useExtensionsStore((state) => state.error);
    const load = useExtensionsStore((state) => state.load);

    useEffect(() => {
        void load();
    }, [load]);

    return { loaded, error };
}