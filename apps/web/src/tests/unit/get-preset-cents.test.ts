import { describe, expect, it } from "vitest";

import { getPresetCents } from "@/lib/topup/get-preset-cents";

describe("getPresetCents", () => {
    it("offers $5, $10, and $20", () => {
        expect(getPresetCents({ minCents: 100, maxCents: 5000, stepCents: 25, creditsPerStep: 2 })).toEqual([
            500, 1000, 2000,
        ]);
    });

    it("leaves out presets above the maximum", () => {
        expect(getPresetCents({ minCents: 100, maxCents: 1000, stepCents: 25, creditsPerStep: 2 })).toEqual([
            500, 1000,
        ]);
    });
});