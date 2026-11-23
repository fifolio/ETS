import { describe, expect, it } from "vitest";

import { describeCredits } from "@/lib/plans/describe-credits";

describe("describeCredits", () => {
    it("describes the monthly credits", () => {
        expect(describeCredits(150)).toBe("150 credits per month");
    });

    it("works for the free plan", () => {
        expect(describeCredits(15)).toBe("15 credits per month");
    });
});