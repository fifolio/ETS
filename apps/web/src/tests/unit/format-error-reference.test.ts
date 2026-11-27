import { describe, expect, it } from "vitest";

import { formatErrorReference } from "@/lib/errors/format-error-reference";

describe("formatErrorReference", () => {
    it("turns the digest into a line the user can quote", () => {
        expect(formatErrorReference("abc123")).toBe("Reference: abc123");
    });

    it("says nothing when there is no digest", () => {
        expect(formatErrorReference(undefined)).toBe("");
        expect(formatErrorReference("")).toBe("");
    });
});