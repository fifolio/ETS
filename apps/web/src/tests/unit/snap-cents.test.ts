import { describe, expect, it } from "vitest";

import { snapCents } from "@/lib/topup/snap-cents";

const limits = { minCents: 100, maxCents: 5000, stepCents: 25, creditsPerStep: 2 };

describe("snapCents", () => {
    it("keeps an amount that is already on a step", () => {
        expect(snapCents(525, limits)).toBe(525);
    });

    it("rounds down to the nearest step", () => {
        expect(snapCents(510, limits)).toBe(500);
    });

    it("rounds up to the nearest step", () => {
        expect(snapCents(513, limits)).toBe(525);
    });

    it("raises an amount below the minimum to the minimum", () => {
        expect(snapCents(90, limits)).toBe(100);
    });

    it("lowers an amount above the maximum to the maximum", () => {
        expect(snapCents(6000, limits)).toBe(5000);
    });
});