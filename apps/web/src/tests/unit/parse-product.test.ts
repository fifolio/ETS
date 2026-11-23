import { describe, expect, it } from "vitest";

import { parseProduct } from "@/lib/checkout/parse-product";

describe("parseProduct", () => {
    it.each(["nextmove", "urgent", "topup"])("accepts %s", (value) => {
        expect(parseProduct(value)).toBe(value);
    });

    it("rejects an unknown product", () => {
        expect(parseProduct("platinum")).toBeNull();
    });

    it("rejects a missing product", () => {
        expect(parseProduct(null)).toBeNull();
    });
});