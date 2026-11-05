"use client";

import { getSetupDeadline } from "@/lib/onboarding/get-setup-deadline";
import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function SetupDeadlineNotice() {
    const user = useAuthStore((state) => state.user);
    const status = useOnboardingStore((state) => state.status);

    if (!user || !status || (status.steps.verify && status.steps.cv)) {
        return null;
    }
    const deadline = getSetupDeadline(user.$createdAt);

    return (
        <p>
            Verify your email and upload your CV before {deadline.toLocaleString()}, or your account is
            deleted automatically.
        </p>
    );
}