"use client";

import { useDialogOpen } from "@/hooks/use-dialog-open";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";

import { FeedbackForm } from "./feedback-form";
import { FeedbackThanks } from "./feedback-thanks";

export function FeedbackModal() {
    const eligible = useFeedbackStore((state) => state.eligible);
    const submitted = useFeedbackStore((state) => state.submitted);
    const dismissed = useFeedbackStore((state) => state.dismissed);
    const dismiss = useFeedbackStore((state) => state.dismiss);
    const ref = useDialogOpen(!dismissed && (eligible || submitted));

    return (
        <dialog ref={ref} onClose={dismiss} aria-labelledby="feedback-title">
            {submitted ? <FeedbackThanks /> : <FeedbackForm />}
        </dialog>
    );
}