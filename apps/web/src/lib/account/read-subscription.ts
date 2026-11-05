import { SUBSCRIPTION_PLANS } from "@/constants/account-defaults";
import type { SubscriptionPlan } from "@/types/account";
import type { AppUser } from "@/types/auth/auth";

/** The plan comes from labels only the server can set, so users can't give themselves one. */
export function readSubscription(user: AppUser): SubscriptionPlan {
  return [...SUBSCRIPTION_PLANS].reverse().find((plan) => user.labels.includes(plan)) ?? "explore";
}