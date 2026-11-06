"use client";

import { useFeedbackStore } from "@/stores/feedback/feedback-store";

export function FeedbackThanks() {
    const dismiss = useFeedbackStore((state) => state.dismiss);

    return (
        <div>
            <h2 id="feedback-title">Thank you!</h2>
            <p>Your feedback was received. Testimonials are reviewed before they appear on the website.</p>
            <button type="button" onClick={dismiss}>
                Close
            </button>
        </div>
    );
}