export function formatCash(amountUsd: number, symbol = "$", rateFromUsd = 1): string {
    const converted = amountUsd * rateFromUsd;
    const fractionDigits = symbol === "$" && rateFromUsd === 1 ? 0 : 2;
    return `${symbol}${new Intl.NumberFormat("en-US", {
        minimumFractionDigits: fractionDigits,
        maximumFractionDigits: fractionDigits,
    }).format(converted)}`;
}