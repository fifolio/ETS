import { describe, expect, it } from "vitest";

import { getEmbedEnvironment } from "@/lib/checkout/get-embed-environment";

describe("getEmbedEnvironment", () => {
    it("tells the embed it runs in the sandbox", () => {
        expect(getEmbedEnvironment("sandbox")).toBe("sandbox");
    });

    it("leaves the embed on its default (production) otherwise", () => {
        expect(getEmbedEnvironment("production")).toBeUndefined();
    });
});