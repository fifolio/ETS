import { describe, expect, it } from "vitest";

import { countScansLeft } from "@/lib/credits/count-scans-left";

describe("countScansLeft", () => {
    it("divides the credits by the cost of a scan", () => {
        expect(countScansLeft(15, 1)).toBe(15);
        expect(countScansLeft(15, 2)).toBe(7);
    });

    it("is zero without credits", () => {
        expect(countScansLeft(0, 1)).toBe(0);
    });

    it("is zero when the cost of a scan is not positive", () => {
        expect(countScansLeft(10, 0)).toBe(0);
    });
});