import { describe, expect, it } from "vitest";

import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import type { AppUser } from "@/types/auth/auth";

const makeUser = (prefs: object) => ({ prefs }) as unknown as AppUser;

describe("readProfilePrefs", () => {
    it("reads saved answers", () => {
        const prefs = readProfilePrefs(
            makeUser({
                role: "Software engineer",
                seniority: "senior",
                yearsOfExperience: 8,
                currentLocation: "Tunis, Tunisia",
                desiredLocations: ["Berlin", "Paris"],
                workArrangements: ["remote"],
                employmentTypes: ["contract"],
                willingToRelocate: true,
                hourlyRate: 40,
                currency: "EUR",
            }),
        );

        expect(prefs).toMatchObject({
            role: "Software engineer",
            seniority: "senior",
            yearsOfExperience: 8,
            desiredLocations: ["Berlin", "Paris"],
            willingToRelocate: true,
            hourlyRate: 40,
            currency: "EUR",
        });
    });

    it("returns empty values and defaults when nothing is saved", () => {
        expect(readProfilePrefs(makeUser({}))).toEqual({
            role: "",
            seniority: "",
            yearsOfExperience: null,
            currentLocation: "",
            desiredLocations: [],
            workArrangements: [],
            employmentTypes: [],
            willingToRelocate: false,
            hourlyRate: null,
            currency: "USD",
        });
    });

    it("ignores a seniority that isn't one of the known levels", () => {
        expect(readProfilePrefs(makeUser({ seniority: "wizard" })).seniority).toBe("");
    });

    it("drops unknown values from the lists", () => {
        const prefs = readProfilePrefs(
            makeUser({ workArrangements: ["remote", "teleport"], desiredLocations: ["Paris", 42] }),
        );

        expect(prefs.workArrangements).toEqual(["remote"]);
        expect(prefs.desiredLocations).toEqual(["Paris"]);
    });
});