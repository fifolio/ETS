"use client";

import { useOnboardingRedirect } from "@/hooks/use-onboarding-redirect";
import { useOnboardingSync } from "@/hooks/use-onboarding-sync";

/** Keeps the setup status fresh and sends the user where the setup rules say. */
export function OnboardingInitializer() {
    useOnboardingSync();
    useOnboardingRedirect();
    return null;
}