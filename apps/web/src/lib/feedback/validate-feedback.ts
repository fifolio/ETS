import { MAX_QUOTE_LENGTH, MAX_SUGGESTIONS_LENGTH } from "@/constants/feedback";
import type { FeedbackInput } from "@/types/feedback";

/** Returns a message for the first problem found, or null when the feedback can be sent. */
export function validateFeedback(input: FeedbackInput): string | null {
    const quote = input.quote.trim();
    const suggestions = input.internal_suggestions.trim();

    if (!quote && !suggestions) {
        return "Write a testimonial, a suggestion, or both.";
    }
    if (quote.length > MAX_QUOTE_LENGTH) {
        return `Your testimonial can have at most ${MAX_QUOTE_LENGTH} characters.`;
    }
    if (suggestions.length > MAX_SUGGESTIONS_LENGTH) {
        return `Your suggestions can have at most ${MAX_SUGGESTIONS_LENGTH} characters.`;
    }
    if (quote && !input.consent) {
        return "Tick the box to allow your testimonial to be shown publicly.";
    }
    return null;
}