import { formatUsd } from "@/lib/topup/format-usd";
import type { TopupPresetsProps } from "@/types/topup";

export function TopupPresets({ presets, selected, onPick }: TopupPresetsProps) {
  return (
    <p>
      {presets.map((cents) => (
        <button
          key={cents}
          type="button"
          aria-pressed={selected === cents}
          onClick={() => onPick(cents)}
        >
          {formatUsd(cents)}
        </button>
      ))}
    </p>
  );
}
