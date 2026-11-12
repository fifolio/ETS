import { describe, expect, it } from "vitest";

import { formatPlanPrice } from "@/lib/plans/format-plan-price";

describe("formatPlanPrice", () => {
    it("says Free for a price of zero", () => {
        expect(formatPlanPrice(0)).toBe("Free");
    });

    it("says the price is coming when it isn't set", () => {
        expect(formatPlanPrice(null)).toBe("Price announced soon");
    });

    it("shows a monthly price in dollars", () => {
        expect(formatPlanPrice(9.99)).toBe("$9.99 per month");
    });
});