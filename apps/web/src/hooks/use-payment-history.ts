import { useBillingData } from "@/hooks/use-billing-data";
import { getPaymentHistory } from "@/services/billing/get-payment-history";

export function usePaymentHistory() {
  return useBillingData(getPaymentHistory, "Could not load your payments.");
}