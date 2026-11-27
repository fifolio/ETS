import { CREDIT_CHANGE_OPTIONS, CREDIT_KIND_OPTIONS } from "@/lib/billing/history-filter-options";
import type { CreditHistoryFiltersProps } from "@/types/history-filters";

import { FilterSelect } from "./filter-select";

export function CreditHistoryFilters({ filters, onChange }: CreditHistoryFiltersProps) {
  return (
    <p>
      <FilterSelect
        label="Type"
        value={filters.kind}
        options={CREDIT_KIND_OPTIONS}
        onChange={(kind) => onChange({ ...filters, kind })}
      />{" "}
      <FilterSelect
        label="Change"
        value={filters.change}
        options={CREDIT_CHANGE_OPTIONS}
        onChange={(change) => onChange({ ...filters, change })}
      />
    </p>
  );
}