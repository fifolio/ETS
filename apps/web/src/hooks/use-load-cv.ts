import { useEffect, useState } from "react";

import { useCvStore } from "@/stores/cv/cv-store";

export function useLoadCv() {
    const loaded = useCvStore((state) => state.loaded);
    const load = useCvStore((state) => state.load);
    const [error, setError] = useState("");

    useEffect(() => {
        load().catch((err: unknown) =>
            setError(err instanceof Error ? err.message : "Could not load your CV."),
        );
    }, [load]);

    return { loaded, error };
}