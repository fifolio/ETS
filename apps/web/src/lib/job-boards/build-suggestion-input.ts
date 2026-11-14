import { readOptionalText } from "@/lib/form/read-optional-text";
import type { SuggestionInput } from "@/types/suggestions";

export function buildSuggestionInput(data: FormData): SuggestionInput {
    return {
        name: String(data.get("name") ?? "").trim(),
        url: String(data.get("url") ?? "").trim(),
        example_url: readOptionalText(data.get("exampleUrl")),
        country: readOptionalText(data.get("country")),
        notes: readOptionalText(data.get("notes")),
    };
}