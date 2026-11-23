import { formatUsd } from "@/lib/topup/format-usd";
import { parseAmountText } from "@/lib/topup/parse-amount-text";
import { snapCents } from "@/lib/topup/snap-cents";
import type { AmountInputResult, TopupLimits } from "@/types/topup";

export function applyTextInput(text: string, limits: TopupLimits): AmountInputResult {
    const cents = parseAmountText(text);
    if (cents === null) {
        return { cents: null, error: "Enter an amount in dollars, for example 5 or 5.25." };
    }
    if (cents < limits.minCents || cents > limits.maxCents) {
        return {
            cents: null,
            error: `Choose an amount between ${formatUsd(limits.minCents)} and ${formatUsd(limits.maxCents)}.`,
        };
    }
    return { cents: snapCents(cents, limits), error: "" };
}