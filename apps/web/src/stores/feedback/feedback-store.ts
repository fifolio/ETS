import { create } from "zustand";

import { ApiRequestError } from "@/lib/api/api-request-error";
import { checkFeedbackEligibility } from "@/services/feedback/check-feedback-eligibility";
import { submitFeedback } from "@/services/feedback/submit-feedback";
import type { FeedbackStore } from "@/types/feedback-store";

export const useFeedbackStore = create<FeedbackStore>()((set) => ({
    eligible: false,
    submitted: false,
    dismissed: false,

    check: async () => {
        try {
            set({ eligible: (await checkFeedbackEligibility()).eligible });
        } catch {
            set({ eligible: false }); // never bother the user because of a failed check
        }
    },
    submit: async (input) => {
        try {
            await submitFeedback(input);
        } catch (error) {
            if (error instanceof ApiRequestError && error.status === 409) {
                set({ eligible: false }); // already sent earlier, so nothing more to ask
                return;
            }
            throw error;
        }
        set({ submitted: true, eligible: false });
    },
    dismiss: () => set({ dismissed: true }),
    clear: () => set({ eligible: false, submitted: false, dismissed: false }),
}));