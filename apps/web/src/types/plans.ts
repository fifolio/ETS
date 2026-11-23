import type { SubscriptionPlan } from "./account";
import { TopupConfig } from "./topup";

export interface PlanInfo {
    id: SubscriptionPlan;
    name: string;
    price_usd_per_month: number | null;
    job_board_count: number;
    monthly_credits: number; 
}

export interface PlansResponse {
    plans: PlanInfo[];
    payments_enabled: boolean;
    topup: TopupConfig;
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