"use client";

import { buildSetupSteps } from "@/lib/profile/build-setup-steps";
import { useAuthStore } from "@/stores/auth/auth-store";
import { useCvStore } from "@/stores/cv/cv-store";

export function SetupChecklist() {
    const user = useAuthStore((state) => state.user);
    const info = useCvStore((state) => state.info);

    if (!user) {
        return null;
    }
    const steps = buildSetupSteps(user, info !== null);

    return (
        <section>
            <h2>Setup</h2>
            <ul>
                {steps.map((step) => (
                    <li key={step.label}>
                        {step.done ? "[x]" : "[ ]"} {step.label}
                    </li>
                ))}
            </ul>
        </section>
    );
}