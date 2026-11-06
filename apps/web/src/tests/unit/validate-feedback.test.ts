import { describe, expect, it } from "vitest";

import { MAX_QUOTE_LENGTH } from "@/constants/feedback";
import { validateFeedback } from "@/lib/feedback/validate-feedback";

const valid = { quote: "Saved me hours.", internal_suggestions: "", consent: true };

describe("validateFeedback", () => {
    it("accepts a testimonial with consent", () => {
        expect(validateFeedback(valid)).toBeNull();
    });

    it("accepts private suggestions alone, without consent", () => {
        expect(
            validateFeedback({ quote: "", internal_suggestions: "Add Safari.", consent: false }),
        ).toBeNull();
    });

    it("rejects an empty form", () => {
        expect(validateFeedback({ quote: " ", internal_suggestions: " ", consent: false })).toMatch(
            /Write a testimonial/,
        );
    });

    it("rejects a testimonial over the maximum length", () => {
        expect(validateFeedback({ ...valid, quote: "x".repeat(MAX_QUOTE_LENGTH + 1) })).toBe(
            `Your testimonial can have at most ${MAX_QUOTE_LENGTH} characters.`,
        );
    });

    it("rejects suggestions over 2000 characters", () => {
        const input = { quote: "", internal_suggestions: "x".repeat(2001), consent: false };
        expect(validateFeedback(input)).toMatch(/2000/);
    });

    it("rejects a testimonial without consent", () => {
        expect(validateFeedback({ ...valid, consent: false })).toMatch(/Tick the box/);
    });
});