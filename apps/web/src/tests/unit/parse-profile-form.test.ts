import { describe, expect, it } from "vitest";

import { parseProfileForm } from "@/lib/profile/parse-profile-form";

function makeForm(entries: Record<string, string | string[]>): FormData {
    const data = new FormData();
    for (const [key, value] of Object.entries(entries)) {
        for (const item of Array.isArray(value) ? value : [value]) {
            data.append(key, item);
        }
    }
    return data;
}

describe("parseProfileForm", () => {
    it("reads every answer", () => {
        const profile = parseProfileForm(
            makeForm({
                seniority: "mid",
                yearsOfExperience: "5",
                currentLocation: " Tunis, Tunisia ",
                desiredLocations: "Paris, Berlin",
                workArrangements: ["remote", "hybrid"],
                employmentTypes: ["full-time"],
                willingToRelocate: "on",
            }),
        );

        expect(profile).toEqual({
            seniority: "mid",
            yearsOfExperience: 5,
            currentLocation: "Tunis, Tunisia",
            desiredLocations: ["Paris", "Berlin"],
            workArrangements: ["remote", "hybrid"],
            employmentTypes: ["full-time"],
            willingToRelocate: true,
        });
    });

    it("splits desired locations on commas and new lines and drops blanks and duplicates", () => {
        const profile = parseProfileForm(makeForm({ desiredLocations: "Paris, Berlin\nParis,  ,Rome" }));

        expect(profile.desiredLocations).toEqual(["Paris", "Berlin", "Rome"]);
    });

    it("uses safe defaults for empty fields", () => {
        const profile = parseProfileForm(makeForm({ yearsOfExperience: "" }));

        expect(profile).toMatchObject({ yearsOfExperience: null, willingToRelocate: false });
    });
});