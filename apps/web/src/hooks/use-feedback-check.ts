import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function useFeedbackCheck(): void {
    const userId = useAuthStore((state) => state.user?.$id);
    const setupComplete = useOnboardingStore((state) => state.status?.complete ?? false);
    const check = useFeedbackStore((state) => state.check);

    useEffect(() => {
        if (userId && setupComplete) {
            void check();
        }
    }, [userId, setupComplete, check]);
}