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
    it("reads every field", () => {
        const profile = parseProfileForm(
            makeForm({
                role: " Nurse ",
                seniority: "mid",
                yearsOfExperience: "5",
                currentLocation: " Tunis, Tunisia ",
                desiredLocations: "Paris, Berlin",
                workArrangements: ["remote", "hybrid"],
                employmentTypes: ["full-time"],
                willingToRelocate: "on",
                hourlyRate: "25.5",
                currency: "EUR",
            }),
        );

        expect(profile).toEqual({
            role: "Nurse",
            seniority: "mid",
            yearsOfExperience: 5,
            currentLocation: "Tunis, Tunisia",
            desiredLocations: ["Paris", "Berlin"],
            workArrangements: ["remote", "hybrid"],
            employmentTypes: ["full-time"],
            willingToRelocate: true,
            hourlyRate: 25.5,
            currency: "EUR",
        });
    });

    it("splits desired locations on commas and new lines and drops blanks and duplicates", () => {
        const profile = parseProfileForm(makeForm({ desiredLocations: "Paris, Berlin\nParis,  ,Rome" }));

        expect(profile.desiredLocations).toEqual(["Paris", "Berlin", "Rome"]);
    });

    it("uses safe defaults for empty optional fields", () => {
        const profile = parseProfileForm(makeForm({ yearsOfExperience: "", hourlyRate: "" }));

        expect(profile).toMatchObject({
            yearsOfExperience: null,
            hourlyRate: null,
            willingToRelocate: false,
            currency: "USD",
        });
    });
});