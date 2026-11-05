import { ONBOARDING_STEP_LABELS } from "@/constants/onboarding";
import type { OnboardingStepName, StepListProps } from "@/types/onboarding/onboarding";

export function StepList({ status }: StepListProps) {
    const names = Object.keys(status.steps) as OnboardingStepName[];

    return (
        <ol>
            {names.map((name) => (
                <li key={name}>
                    {status.steps[name] ? "[x]" : "[ ]"} {ONBOARDING_STEP_LABELS[name]}
                    {status.next_step === name ? " (current)" : ""}
                </li>
            ))}
        </ol>
    );
}