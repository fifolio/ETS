import { useBillingData } from "@/hooks/use-billing-data";
import { getCredits } from "@/services/credits/get-credits";

export function useCredits() {
  const { data, error } = useBillingData(getCredits, "Could not load your credits.");
  return { credits: data, error };
}