import type { TopupLimits } from "@/types/topup";

const PRESET_CENTS = [500, 1000, 2000];

export function getPresetCents(limits: TopupLimits): number[] {
    return PRESET_CENTS.filter(
        (cents) => cents >= limits.minCents && cents <= limits.maxCents && cents % limits.stepCents === 0,
    );
}