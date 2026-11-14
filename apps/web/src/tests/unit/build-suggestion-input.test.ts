import { describe, expect, it } from "vitest";

import { buildSuggestionInput } from "@/lib/job-boards/build-suggestion-input";

function makeForm(entries: Record<string, string>): FormData {
    const data = new FormData();
    for (const [key, value] of Object.entries(entries)) {
        data.append(key, value);
    }
    return data;
}

describe("buildSuggestionInput", () => {
    it("trims the fields and maps the form names", () => {
        const input = buildSuggestionInput(
            makeForm({
                name: " Wellfound ",
                url: " https://wellfound.com/jobs ",
                exampleUrl: " https://wellfound.com/jobs/1 ",
                country: " Canada ",
                notes: " Startups ",
            }),
        );

        expect(input).toEqual({
            name: "Wellfound",
            url: "https://wellfound.com/jobs",
            example_url: "https://wellfound.com/jobs/1",
            country: "Canada",
            notes: "Startups",
        });
    });

    it("turns empty optional fields into null", () => {
        const input = buildSuggestionInput(
            makeForm({ name: "Wellfound", url: "https://wellfound.com/jobs", exampleUrl: " ", notes: "" }),
        );

        expect(input).toMatchObject({ example_url: null, country: null, notes: null });
    });
});