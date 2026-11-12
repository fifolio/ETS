"use client";

import { usePlans } from "@/hooks/use-plans";
import { useUpgrade } from "@/hooks/use-upgrade";
import { readSubscription } from "@/lib/account/read-subscription";
import { useAuthStore } from "@/stores/auth/auth-store";

import { PlanList } from "./plan-list";

export function SubscriptionSection() {
    const user = useAuthStore((state) => state.user);
    const { plans, paymentsEnabled, error, loaded } = usePlans();
    const { busy, error: upgradeError, upgrade } = useUpgrade();

    if (!user) {
        return null;
    }
    const currentPlan = readSubscription(user);
    const currentName = plans.find((plan) => plan.id === currentPlan)?.name ?? currentPlan;

    return (
        <section>
            <h2>Subscription</h2>
            <p>Your plan: {currentName}</p>
            {error && <p role="alert">{error}</p>}
            {!loaded && !error && <p>Loading...</p>}
            {loaded && (
                <PlanList
                    plans={plans}
                    currentPlan={currentPlan}
                    paymentsEnabled={paymentsEnabled}
                    busy={busy}
                    onUpgrade={upgrade}
                />
            )}
            {upgradeError && <p role="alert">{upgradeError}</p>}
        </section>
    );
}