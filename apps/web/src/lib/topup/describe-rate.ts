import { formatUsd } from "@/lib/topup/format-usd";
import type { TopupConfig } from "@/types/topup";

export function describeRate(config: TopupConfig): string {
    return `${formatUsd(100)} = ${config.credits_per_usd} credits`;
}