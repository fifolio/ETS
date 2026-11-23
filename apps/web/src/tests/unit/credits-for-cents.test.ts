import { describe, expect, it } from "vitest";

import { creditsForCents } from "@/lib/topup/credits-for-cents";

const limits = { minCents: 100, maxCents: 5000, stepCents: 25, creditsPerStep: 2 };

describe("creditsForCents", () => {
    it.each([
        [100, 8],
        [125, 10],
        [200, 16],
        [500, 40],
        [1000, 80],
        [2000, 160],
        [5000, 400],
    ])("%i cents buys %i credits", (cents, credits) => {
        expect(creditsForCents(cents, limits)).toBe(credits);
    });

    it("follows 8 credits per dollar on every step", () => {
        for (let cents = 100; cents <= 5000; cents += 25) {
            expect(creditsForCents(cents, limits) * 12.5).toBe(cents);
        }
    });
});