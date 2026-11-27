export type CreditKindFilter = "all" | "subscription" | "promotional" | "purchased";
export type CreditChangeFilter = "all" | "added" | "used";
export type PaymentStatusFilter = "all" | "completed" | "failed" | "underpaid" | "refunded";
export type PaymentProductFilter = "all" | "plan" | "topup";

export interface CreditFilters {
    kind: CreditKindFilter;
    change: CreditChangeFilter;
}

export interface PaymentFilters {
    status: PaymentStatusFilter;
    product: PaymentProductFilter;
}

export interface FilterOption<T extends string> {
    value: T;
    label: string;
}

export interface FilterSelectProps<T extends string> {
    label: string;
    value: T;
    options: FilterOption<T>[];
    onChange: (value: T) => void;
}

export interface CreditHistoryFiltersProps {
    filters: CreditFilters;
    onChange: (filters: CreditFilters) => void;
}

export interface PaymentHistoryFiltersProps {
    filters: PaymentFilters;
    onChange: (filters: PaymentFilters) => void;
}