import { useBillingData } from "@/hooks/use-billing-data";
import { getSubscriptionStatus } from "@/services/billing/get-subscription-status";

export function useSubscriptionStatus() {
  return useBillingData(getSubscriptionStatus, "Could not load your subscription.");
}