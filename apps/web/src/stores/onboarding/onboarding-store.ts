import { create } from "zustand";

import { getOnboardingStatus } from "@/services/onboarding/get-onboarding-status";
import type { OnboardingStore } from "@/types/onboarding/onboarding-store";

export const useOnboardingStore = create<OnboardingStore>()((set) => ({
    status: null,
    error: "",

    load: async () => {
        try {
            set({ status: await getOnboardingStatus(), error: "" });
        } catch (err) {
            set({ error: err instanceof Error ? err.message : "Could not reach the server." });
        }
    },
    clear: () => set({ status: null, error: "" }),
}));