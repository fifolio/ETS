import { describe, expect, it } from "vitest";

import { describeCredits } from "@/lib/plans/describe-credits";

describe("describeCredits", () => {
    it("describes the monthly credits and the top-up", () => {
        expect(describeCredits(150, 25, 2)).toBe("150 credits per month. Top-up: 25 credits for $2.");
    });

    it("works for the free plan", () => {
        expect(describeCredits(15, 25, 3)).toBe("15 credits per month. Top-up: 25 credits for $3.");
    });
});