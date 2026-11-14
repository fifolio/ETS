import { MIN_NAME_LENGTH } from "@/constants/suggestions";
import { getSiteHost } from "@/lib/job-boards/get-site-host";
import { parseWebAddress } from "@/lib/job-boards/parse-web-address";
import type { SuggestionInput } from "@/types/suggestions";

/** Returns a message for the first problem found, or null when the suggestion can be sent. */
export function validateSuggestion(input: SuggestionInput): string | null {
    if (input.name.trim().length < MIN_NAME_LENGTH) {
        return "Enter the name of the job board.";
    }
    const url = parseWebAddress(input.url);
    if (!url) {
        return "Enter a valid web address that starts with http:// or https://.";
    }
    if (input.example_url) {
        const example = parseWebAddress(input.example_url);
        if (!example) {
            return "The example job link isn't a valid web address.";
        }
        if (getSiteHost(example) !== getSiteHost(url)) {
            return "The example job link must be on the same website as the job board.";
        }
    }
    return null;
}