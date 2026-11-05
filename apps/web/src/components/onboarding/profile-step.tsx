"use client";

import { ProfileForm } from "@/components/profile/profile-form";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

import { MissingFields } from "./missing-fields";

export function ProfileStep() {
    const missing = useOnboardingStore((state) => state.status?.missing_profile_fields ?? []);

    return (
        <div>
            <h2>Let us learn more about you and tell us what you are looking for</h2>
            <ProfileForm />
            <MissingFields fields={missing} />
        </div>
    );
}