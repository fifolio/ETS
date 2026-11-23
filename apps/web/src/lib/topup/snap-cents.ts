import type { TopupLimits } from "@/types/topup";

/** The nearest allowed amount: inside the range and on a step. */
export function snapCents(cents: number, limits: TopupLimits): number {
    const clamped = Math.min(Math.max(cents, limits.minCents), limits.maxCents);
    const snapped = Math.round(clamped / limits.stepCents) * limits.stepCents;
    return Math.min(Math.max(snapped, limits.minCents), limits.maxCents);
}