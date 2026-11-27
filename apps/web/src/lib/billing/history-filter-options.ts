import type {
    CreditChangeFilter,
    CreditFilters,
    CreditKindFilter,
    FilterOption,
    PaymentFilters,
    PaymentProductFilter,
    PaymentStatusFilter,
} from "@/types/history-filters";

export const CREDIT_KIND_OPTIONS: FilterOption<CreditKindFilter>[] = [
    { value: "all", label: "All types" },
    { value: "subscription", label: "Monthly allowance" },
    { value: "promotional", label: "Welcome bonus" },
    { value: "purchased", label: "Purchased" },
];

export const CREDIT_CHANGE_OPTIONS: FilterOption<CreditChangeFilter>[] = [
    { value: "all", label: "All changes" },
    { value: "added", label: "Added (+)" },
    { value: "used", label: "Used or removed (-)" },
];

export const PAYMENT_STATUS_OPTIONS: FilterOption<PaymentStatusFilter>[] = [
    { value: "all", label: "All statuses" },
    { value: "completed", label: "Paid" },
    { value: "failed", label: "Failed" },
    { value: "underpaid", label: "Underpaid" },
    { value: "refunded", label: "Refunded" },
];

export const PAYMENT_PRODUCT_OPTIONS: FilterOption<PaymentProductFilter>[] = [
    { value: "all", label: "All products" },
    { value: "plan", label: "Plans" },
    { value: "topup", label: "Top-ups" },
];

export const DEFAULT_CREDIT_FILTERS: CreditFilters = { kind: "all", change: "all" };
export const DEFAULT_PAYMENT_FILTERS: PaymentFilters = { status: "all", product: "all" };