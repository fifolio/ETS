export function describeCredits(monthly: number, topupCredits: number, topupPriceUsd: number): string {
  return `${monthly} credits per month. Top-up: ${topupCredits} credits for $${topupPriceUsd}.`;
} 