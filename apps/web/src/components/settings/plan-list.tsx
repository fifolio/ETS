import { canUpgradeTo } from "@/lib/plans/can-upgrade-to";
import type { PlanListProps } from "@/types/plans";

import { PlanCard } from "./plan-card";

export function PlanList({ plans, currentPlan, paymentsEnabled, busy, onUpgrade }: PlanListProps) {
    return (
        <ul>
            {plans.map((plan) => (
                <PlanCard
                    key={plan.id}
                    plan={plan}
                    current={plan.id === currentPlan}
                    upgradable={canUpgradeTo(currentPlan, plan.id)}
                    paymentsEnabled={paymentsEnabled}
                    busy={busy}
                    onUpgrade={onUpgrade}
                />
            ))}
        </ul>
    );
}