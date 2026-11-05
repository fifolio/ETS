import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function useOnboardingSync(): void {
    const userId = useAuthStore((state) => state.user?.$id);
    const verified = useAuthStore((state) => state.user?.emailVerification);
    const load = useOnboardingStore((state) => state.load);

    useEffect(() => {
        if (userId) {
            void load();
        }
    }, [userId, verified, load]);
}