"use client";

import { useTopupAmount } from "@/hooks/use-topup-amount";
import { describeRate } from "@/lib/topup/describe-rate";
import { formatUsd } from "@/lib/topup/format-usd";
import { getPresetCents } from "@/lib/topup/get-preset-cents";
import { getTopupLimits } from "@/lib/topup/get-topup-limits";
import type { TopupPickerProps } from "@/types/topup";

import { TopupPresets } from "./topup-presets";

export function TopupPicker({ config, onContinue }: TopupPickerProps) {
  const limits = getTopupLimits(config);
  const amount = useTopupAmount(limits);

  return (
    <div>
      <h2>{formatUsd(amount.cents)}</h2>
      <p>{amount.credits} credits</p>
      <input
        type="range"
        aria-label="Top-up amount"
        min={limits.minCents}
        max={limits.maxCents}
        step={limits.stepCents}
        value={amount.cents}
        onChange={(event) => amount.setFromSlider(Number(event.target.value))}
      />
      <p>
        {formatUsd(limits.minCents)} to {formatUsd(limits.maxCents)}, in steps
        of {formatUsd(limits.stepCents)}. Rate: {describeRate(config)}, the same
        on every plan.
      </p>
      <TopupPresets
        presets={getPresetCents(limits)}
        selected={amount.cents}
        onPick={amount.setFromSlider}
      />
      <label>
        Or type an amount in dollars{" "}
        <input
          inputMode="decimal"
          value={amount.text}
          onChange={(event) => amount.setFromText(event.target.value)}
          onBlur={amount.commitText}
        />
      </label>
      {amount.error && <p role="alert">{amount.error}</p>}
      <p>
        You will pay {formatUsd(amount.cents)} for {amount.credits} credits.
      </p>
      <button
        type="button"
        disabled={Boolean(amount.error)}
        onClick={() => onContinue(amount.cents)}
      >
        Continue to payment
      </button>
    </div>
  );
}
