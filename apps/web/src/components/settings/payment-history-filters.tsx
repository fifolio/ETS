import { PAYMENT_PRODUCT_OPTIONS, PAYMENT_STATUS_OPTIONS } from "@/lib/billing/history-filter-options";
import type { PaymentHistoryFiltersProps } from "@/types/history-filters";

import { FilterSelect } from "./filter-select";

export function PaymentHistoryFilters({ filters, onChange }: PaymentHistoryFiltersProps) {
  return (
    <p>
      <FilterSelect
        label="Status"
        value={filters.status}
        options={PAYMENT_STATUS_OPTIONS}
        onChange={(status) => onChange({ ...filters, status })}
      />{" "}
      <FilterSelect
        label="Product"
        value={filters.product}
        options={PAYMENT_PRODUCT_OPTIONS}
        onChange={(product) => onChange({ ...filters, product })}
      />
    </p>
  );
}