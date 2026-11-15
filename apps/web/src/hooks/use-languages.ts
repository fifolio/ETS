import { useEffect, useState } from "react";

import { getLanguages } from "@/services/languages/get-languages";
import type { LanguageInfo } from "@/types/language";

export function useLanguages() {
    const [languages, setLanguages] = useState<LanguageInfo[] | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        getLanguages()
            .then(setLanguages)
            .catch(() => setError("Could not load the languages."));
    }, []);

    return { languages, error };
}