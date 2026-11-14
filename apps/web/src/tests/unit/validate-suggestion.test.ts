import { describe, expect, it } from "vitest";

import { validateSuggestion } from "@/lib/job-boards/validate-suggestion";
import type { SuggestionInput } from "@/types/suggestions";

const valid: SuggestionInput = {
    name: "Wellfound",
    url: "https://wellfound.com/jobs",
    example_url: "https://www.wellfound.com/jobs/1234-engineer",
    country: null,
    notes: null,
};

describe("validateSuggestion", () => {
    it("accepts a complete suggestion, ignoring www on the example link", () => {
        expect(validateSuggestion(valid)).toBeNull();
    });

    it("accepts a suggestion without an example link", () => {
        expect(validateSuggestion({ ...valid, example_url: null })).toBeNull();
    });

    it("asks for a name of at least two characters", () => {
        expect(validateSuggestion({ ...valid, name: " x " })).toMatch(/name of the job board/);
    });

    it.each(["", "wellfound", "ftp://wellfound.com/jobs", "http://localhost/jobs"])(
        "rejects %j as the main address",
        (url) => {
            expect(validateSuggestion({ ...valid, url })).toMatch(/valid web address/);
        },
    );

    it("rejects an example link that isn't a web address", () => {
        expect(validateSuggestion({ ...valid, example_url: "not a link" })).toMatch(/isn't a valid/);
    });

    it("rejects an example link on another website", () => {
        expect(validateSuggestion({ ...valid, example_url: "https://other.com/jobs/1" })).toMatch(
            /same website/,
        );
    });
});