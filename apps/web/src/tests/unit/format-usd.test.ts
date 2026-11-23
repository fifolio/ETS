import { describe, expect, it } from "vitest";

import { formatUsd } from "@/lib/topup/format-usd";

describe("formatUsd", () => {
    it.each([
        [100, "$1.00"],
        [525, "$5.25"],
        [5000, "$50.00"],
    ])("%i cents is %s", (cents, text) => {
        expect(formatUsd(cents)).toBe(text);
    });
});