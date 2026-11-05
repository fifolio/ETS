import { describe, expect, it } from "vitest";

import { getSetupDeadline } from "@/lib/onboarding/get-setup-deadline";

describe("getSetupDeadline", () => {
    it("is 48 hours after the account was created", () => {
        expect(getSetupDeadline("2026-11-02T10:00:00.000+00:00").toISOString()).toBe(
            "2026-11-04T10:00:00.000Z",
        );
    });

    it("works across the end of a month", () => {
        expect(getSetupDeadline("2026-11-29T23:00:00.000+00:00").toISOString()).toBe(
            "2026-12-01T23:00:00.000Z",
        );
    });
});