import { describe, expect, it } from "vitest";

import { getTopupLimits } from "@/lib/topup/get-topup-limits";

describe("getTopupLimits", () => {
    it("turns the server's dollars into whole cents", () => {
        const config = { min_usd: 1, max_usd: 50, step_usd: 0.25, credits_per_step: 2, credits_per_usd: 8 };

        expect(getTopupLimits(config)).toEqual({
            minCents: 100,
            maxCents: 5000,
            stepCents: 25,
            creditsPerStep: 2,
        });
    });
});