import { describe, expect, it } from "vitest";

import { buildSetupSteps } from "@/lib/profile/build-setup-steps";
import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import type { AppUser } from "@/types/auth/auth";

const makeUser = (prefs: object, emailVerification = true) =>
    ({ prefs, emailVerification }) as unknown as AppUser;

describe("readProfilePrefs", () => {
    it("reads a saved role and seniority", () => {
        const user = makeUser({ role: "Software engineer", seniority: "senior" });
        expect(readProfilePrefs(user)).toEqual({ role: "Software engineer", seniority: "senior" });
    });

    it("returns empty values when nothing is saved", () => {
        expect(readProfilePrefs(makeUser({}))).toEqual({ role: "", seniority: "" });
    });

    it("ignores a seniority that isn't one of the known levels", () => {
        expect(readProfilePrefs(makeUser({ role: "Nurse", seniority: "wizard" })).seniority).toBe("");
    });
});

describe("buildSetupSteps", () => {
    it("marks every step done for a fully set up user", () => {
        const user = makeUser({ role: "Nurse", seniority: "mid" });
        expect(buildSetupSteps(user, true).every((step) => step.done)).toBe(true);
    });

    it("reports what is missing for a new user", () => {
        const steps = buildSetupSteps(makeUser({}, false), false);
        expect(steps.map((step) => step.done)).toEqual([false, false, false]);
    });
});