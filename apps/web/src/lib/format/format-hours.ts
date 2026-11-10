export function formatHours(value: number): string {
    return new Intl.NumberFormat("en-US", { maximumFractionDigits: 1 }).format(value);
}