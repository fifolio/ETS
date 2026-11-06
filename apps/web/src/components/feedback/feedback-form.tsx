"use client";

import { MAX_QUOTE_LENGTH, MAX_SUGGESTIONS_LENGTH } from "@/constants/feedback";
import { useFeedbackForm } from "@/hooks/use-feedback-form";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";

export function FeedbackForm() {
    const dismiss = useFeedbackStore((state) => state.dismiss);
    const form = useFeedbackForm();

    return (
        <form onSubmit={form.handleSubmit}>
            <h2 id="feedback-title">How is ETS working for you?</h2>
            <p>You have been using ETS for a while. Two quick questions help us a lot.</p>

            <label>
                Public testimonial (optional, shown on our website, up to {MAX_QUOTE_LENGTH} characters)
                <br />
                <textarea
                    value={form.quote}
                    onChange={(event) => form.setQuote(event.target.value)}
                    maxLength={MAX_QUOTE_LENGTH}
                    rows={4}
                />
            </label>
            <p>
                {form.quote.length}/{MAX_QUOTE_LENGTH}
            </p>
            <label>
                <input
                    type="checkbox"
                    checked={form.consent}
                    onChange={(event) => form.setConsent(event.target.checked)}
                />{" "}
                I agree that my testimonial, my first name with the initial of my last name, my role, and
                the time I saved can be shown publicly.
            </label>

            <p>
                <label>
                    Suggestions for us (optional, private: only our team reads this)
                    <br />
                    <textarea
                        value={form.suggestions}
                        onChange={(event) => form.setSuggestions(event.target.value)}
                        maxLength={MAX_SUGGESTIONS_LENGTH}
                        rows={4}
                    />
                </label>
            </p>

            <button type="submit" disabled={form.busy}>
                Send
            </button>{" "}
            <button type="button" onClick={dismiss}>
                Maybe later
            </button>
            {form.error && <p role="alert">{form.error}</p>}
        </form>
    );
}