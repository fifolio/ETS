import type { SubscriptionPlan } from "./account";

export interface PlanInfo {
    id: SubscriptionPlan;
    name: string;
    max_job_boards: number | null;
    price_usd_per_month: number | null;
}

export interface PlansResponse {
    plans: PlanInfo[];
    payments_enabled: boolean;
}

export interface PlanCardProps {
    plan: PlanInfo;
    current: boolean;
    upgradable: boolean;
    paymentsEnabled: boolean;
    busy: boolean;
    onUpgrade: (plan: SubscriptionPlan) => void;
}

export interface PlanListProps {
    plans: PlanInfo[];
    currentPlan: SubscriptionPlan;
    paymentsEnabled: boolean;
    busy: boolean;
    onUpgrade: (plan: SubscriptionPlan) => void;
}