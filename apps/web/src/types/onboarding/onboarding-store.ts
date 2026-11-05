import type { OnboardingStatus } from "./onboarding";

export interface OnboardingState {
    status: OnboardingStatus | null;
    error: string;
}

export interface OnboardingActions {
    load: () => Promise<void>;
    clear: () => void;
}

export type OnboardingStore = OnboardingState & OnboardingActions;