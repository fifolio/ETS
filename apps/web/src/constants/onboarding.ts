import type { OnboardingStepName } from "@/types/onboarding/onboarding";

export const ONBOARDING_STEP_LABELS: Record<OnboardingStepName, string> = {
    verify: "Verify your email",
    cv: "Upload your CV",
    profile: "Let us learn more about you and tell us what you are looking for",
    extension: "Install the extension and log in",
};

// Pages a logged-in user can open before the setup is finished.
export const PAGES_OPEN_DURING_SETUP = ["/setup", "/verify"];