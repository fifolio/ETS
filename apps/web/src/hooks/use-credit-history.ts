import { useCallback, useState } from "react";

import { useBillingData } from "@/hooks/use-billing-data";
import { DEFAULT_CREDIT_FILTERS } from "@/lib/billing/history-filter-options";
import { getCreditHistory } from "@/services/billing/get-credit-history";
import type { CreditFilters } from "@/types/history-filters";

export function useCreditHistory() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<CreditFilters>(DEFAULT_CREDIT_FILTERS);
  const load = useCallback(() => getCreditHistory(page, filters), [page, filters]);
  const { data, error } = useBillingData(load, "Could not load your credit history.");

  function changeFilters(next: CreditFilters) {
    setFilters(next);
    setPage(1); // a new filter starts again at the first page
  }

  return { data, error, filters, setPage, changeFilters };
}