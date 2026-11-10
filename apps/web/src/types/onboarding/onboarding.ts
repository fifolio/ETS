export type OnboardingStepName = "verify" | "cv" | "profile" | "extension";

export interface OnboardingStatus {
    steps: Record<string, boolean>;
    next_step: OnboardingStepName | null;
    complete: boolean;
    missing_profile_fields: string[];
}

export interface StepListProps {
    status: OnboardingStatus;
}

export interface MissingFieldsProps {
    fields: string[];
}