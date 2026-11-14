import { useState } from "react";

import { useFormSubmit } from "@/hooks/use-form-submit";
import { buildSuggestionInput } from "@/lib/job-boards/build-suggestion-input";
import { validateSuggestion } from "@/lib/job-boards/validate-suggestion";
import { submitSuggestion } from "@/services/suggestions/submit-suggestion";
import type { SuggestionReceipt } from "@/types/suggestions";

export function useSuggestionForm() {
    const [receipt, setReceipt] = useState<SuggestionReceipt | null>(null);
    const [version, setVersion] = useState(0);

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        setReceipt(null);
        const input = buildSuggestionInput(data);
        const problem = validateSuggestion(input);
        if (problem) {
            throw new Error(problem);
        }
        setReceipt(await submitSuggestion(input));
        setVersion((value) => value + 1); // a new key empties the form
    });

    return { receipt, version, busy, error, handleSubmit };
}