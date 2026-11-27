import { describe, expect, it } from "vitest";

import { getOnboardingRedirect } from "@/lib/onboarding/get-onboarding-redirect";

describe("getOnboardingRedirect", () => {
    it.each([
        ["leaves a logged-out visitor alone", "/", false, false, null],
        ["sends a user still setting up away from a page", "/history", true, false, "/setup"],
        ["sends a user still setting up away from the home page", "/", true, false, "/setup"],
        ["lets a user still setting up stay on /setup", "/setup", true, false, null],
        ["lets a user still setting up open /verify", "/verify", true, false, null],
        ["sends a finished user away from /setup", "/setup", true, true, "/"],
        ["lets a finished user stay on a normal page", "/history", true, true, null],
    ])("%s", (_name, pathname, loggedIn, complete, expected) => {
        expect(getOnboardingRedirect(pathname, loggedIn, complete)).toBe(expected);
    });
});