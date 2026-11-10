"use client";

import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

import { CvStep } from "./cv-step";
import { ProfileStep } from "./profile-step";
import { StepList } from "./step-list";
import { VerifyStep } from "./verify-step";
import { SetupDeadlineNotice } from "./setup-deadline-notice";
import { ExtensionStep } from "./extension-step";


export function SetupWizard() {
    const status = useOnboardingStore((state) => state.status);
    const error = useOnboardingStore((state) => state.error);

    if (!status) {
        return error ? <p role="alert">{error}</p> : <p>Loading...</p>;
    }

    return (
        <section>
            <StepList status={status} />
            <SetupDeadlineNotice />
            {status.next_step === "verify" && <VerifyStep />}
            {status.next_step === "cv" && <CvStep />}
            {status.next_step === "profile" && <ProfileStep />}
            {status.next_step === "extension" && <ExtensionStep />}
            {status.complete && <p>All set. Taking you to your dashboard...</p>}
        </section>
    );
}