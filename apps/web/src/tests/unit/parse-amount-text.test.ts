import { describe, expect, it } from "vitest";

import { parseAmountText } from "@/lib/topup/parse-amount-text";

describe("parseAmountText", () => {
    it.each([
        ["5", 500],
        ["5.25", 525],
        ["$5.25", 525],
        ["5,25", 525],
        [" 10 ", 1000],
    ])("reads %j as %i cents", (text, cents) => {
        expect(parseAmountText(text)).toBe(cents);
    });

    it.each(["5.256", "abc", "", "-3"])("rejects %j", (text) => {
        expect(parseAmountText(text)).toBeNull();
    });
});