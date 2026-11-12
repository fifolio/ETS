export function formatPlanPrice(price: number | null): string {
    if (price === null) {
        return "Price announced soon";
    }
    if (price === 0) {
        return "Free";
    }
    const amount = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(price);
    return `${amount} per month`;
}