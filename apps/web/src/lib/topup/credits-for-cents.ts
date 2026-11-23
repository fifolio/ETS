import type { TopupLimits } from "@/types/topup";

export function creditsForCents(cents: number, limits: TopupLimits): number {
    return Math.floor(cents / limits.stepCents) * limits.creditsPerStep;
}