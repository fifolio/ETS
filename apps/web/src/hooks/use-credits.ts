import { useEffect, useState } from "react";

import { getCredits } from "@/services/credits/get-credits";
import type { CreditsInfo } from "@/types/credits";

export function useCredits() {
    const [credits, setCredits] = useState<CreditsInfo | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        getCredits()
            .then(setCredits)
            .catch((err) => setError(err instanceof Error ? err.message : "Could not load your credits."));
    }, []);

    return { credits, error };
}