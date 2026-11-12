import { SUBSCRIPTION_PLANS } from "@/constants/account-defaults";
import type { SubscriptionPlan } from "@/types/account";

/** True when `target` is a paid plan above the current one. */
export function canUpgradeTo(current: SubscriptionPlan, target: SubscriptionPlan): boolean {
    return target !== "explore" && SUBSCRIPTION_PLANS.indexOf(target) > SUBSCRIPTION_PLANS.indexOf(current);
}