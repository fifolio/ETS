"use client";

import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

import { LoggedInLinks } from "./logged-in-links";
import { LoggedOutLinks } from "./logged-out-links";
import { SettingUpLinks } from "./setting-up-links";

export function Nav() {
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);
    const setupComplete = useOnboardingStore((state) => state.status?.complete ?? false);

    if (loading) {
        return <nav>ETS</nav>;
    }
    if (!user) {
        return (
            <nav>
                <LoggedOutLinks />
            </nav>
        );
    }
    return <nav>{setupComplete ? <LoggedInLinks name={user.name} /> : <SettingUpLinks name={user.name} />}</nav>;
}