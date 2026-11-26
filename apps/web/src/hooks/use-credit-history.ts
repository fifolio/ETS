import { useBillingData } from "@/hooks/use-billing-data";
import { getCreditHistory } from "@/services/billing/get-credit-history";

export function useCreditHistory() {
  return useBillingData(getCreditHistory, "Could not load your credit history.");
}