import { describe, expect, it } from "vitest";

import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import type { AppUser } from "@/types/auth/auth";

const makeUser = (prefs: object) => ({ prefs }) as unknown as AppUser;

describe("readProfilePrefs", () => {
    it("reads saved answers, including the industry, role, and hourly rate", () => {
        const prefs = readProfilePrefs(
            makeUser({
                industryId: "software-it",
                industry: "Software & IT",
                jobId: "job-1",
                role: "Software engineer",
                hourlyRateUsd: 50,
                seniority: "senior",
                yearsOfExperience: 8,
                currentLocation: "Tunis, Tunisia",
                desiredLocations: ["Berlin", "Paris"],
                workArrangements: ["remote"],
                employmentTypes: ["contract"],
                willingToRelocate: true,
            }),
        );

        expect(prefs).toMatchObject({
            industryId: "software-it",
            industry: "Software & IT",
            jobId: "job-1",
            role: "Software engineer",
            hourlyRateUsd: 50,
            seniority: "senior",
            yearsOfExperience: 8,
            desiredLocations: ["Berlin", "Paris"],
            willingToRelocate: true,
        });
    });

    it("returns empty values when nothing is saved", () => {
        expect(readProfilePrefs(makeUser({}))).toEqual({
            industryId: "",
            industry: "",
            jobId: "",
            role: "",
            hourlyRateUsd: null,
            seniority: "",
            yearsOfExperience: null,
            currentLocation: "",
            desiredLocations: [],
            workArrangements: [],
            employmentTypes: [],
            willingToRelocate: false,
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