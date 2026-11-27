import { useCallback, useState } from "react";

import { useBillingData } from "@/hooks/use-billing-data";
import { DEFAULT_PAYMENT_FILTERS } from "@/lib/billing/history-filter-options";
import { getPaymentHistory } from "@/services/billing/get-payment-history";
import type { PaymentFilters } from "@/types/history-filters";

export function usePaymentHistory() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<PaymentFilters>(DEFAULT_PAYMENT_FILTERS);
  const load = useCallback(() => getPaymentHistory(page, filters), [page, filters]);
  const { data, error } = useBillingData(load, "Could not load your payments.");

  function changeFilters(next: PaymentFilters) {
    setFilters(next);
    setPage(1);
  }

  return { data, error, filters, setPage, changeFilters };
}