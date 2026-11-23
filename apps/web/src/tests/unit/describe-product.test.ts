import { describe, expect, it } from "vitest";

import { describeProduct } from "@/lib/checkout/describe-product";

describe("describeProduct", () => {
    it("names the plans", () => {
        expect(describeProduct("nextmove")).toBe("The Next Move plan");
        expect(describeProduct("urgent")).toBe("The Urgent plan");
    });

    it("names the top-up", () => {
        expect(describeProduct("topup")).toBe("A credit top-up");
    });
});