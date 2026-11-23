import type { TopupConfig, TopupLimits } from "@/types/topup";

export function getTopupLimits(config: TopupConfig): TopupLimits {
    return {
        minCents: Math.round(config.min_usd * 100),
        maxCents: Math.round(config.max_usd * 100),
        stepCents: Math.round(config.step_usd * 100),
        creditsPerStep: config.credits_per_step,
    };
}