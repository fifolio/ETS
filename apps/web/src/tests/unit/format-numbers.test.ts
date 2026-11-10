import { describe, expect, it } from "vitest";

import { formatCash } from "@/lib/format/format-cash";
import { formatCount } from "@/lib/format/format-count";
import { formatHours } from "@/lib/format/format-hours";

describe("number formatting", () => {
    it("groups the thousands of a count", () => {
        expect(formatCount(1234567)).toBe("1,234,567");
    });

    it("keeps one decimal for hours", () => {
        expect(formatHours(1234.56)).toBe("1,234.6");
    });

    it("shows cash in whole dollars", () => {
        expect(formatCash(98765.4)).toBe("$98,765");
    });
});