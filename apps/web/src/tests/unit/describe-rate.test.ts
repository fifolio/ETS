import { describe, expect, it } from "vitest";

import { describeRate } from "@/lib/topup/describe-rate";

describe("describeRate", () => {
    it("states the conversion rate from the server's config", () => {
        const config = { min_usd: 1, max_usd: 50, step_usd: 0.25, credits_per_step: 2, credits_per_usd: 8 };

        expect(describeRate(config)).toBe("$1.00 = 8 credits");
    });
});