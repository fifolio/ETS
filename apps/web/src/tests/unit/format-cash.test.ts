import { describe, expect, it } from "vitest";
import { formatCash } from "@/lib/format/format-cash";

describe("formatCash", () => {
    it("shows USD with no conversion", () => {
        expect(formatCash(10, "$", 1)).toBe("$10");
    });
    it("converts to another currency", () => {
        expect(formatCash(10, "€", 0.92)).toBe("€9.20");
    });
    it("defaults to dollar display", () => {
        expect(formatCash(50)).toBe("$50");
    });
});