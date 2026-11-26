import { describe, expect, it } from "vitest";

import { applyTextInput } from "@/lib/topup/apply-text-input";

const limits = { minCents: 100, maxCents: 5000, stepCents: 25, creditsPerStep: 2 };

describe("applyTextInput", () => {
    it("snaps a typed amount to the nearest step, the same as the slider would", () => {
        expect(applyTextInput("5.10", limits)).toEqual({ cents: 500, error: "" });
    });

    it("explains an amount below the minimum", () => {
        expect(applyTextInput("0.99", limits)).toEqual({
            cents: null,
            error: "Choose an amount between $1.00 and $50.00.",
        });
    });

    it("explains an amount above the maximum", () => {
        expect(applyTextInput("75", limits).error).toMatch(/\$50\.00/);
    });

    it("explains text that isn't an amount", () => {
        expect(applyTextInput("abc", limits).error).toMatch(/Enter an amount/);
    });
});