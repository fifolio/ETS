export interface TopupConfig {
    min_usd: number;
    max_usd: number;
    step_usd: number;
    credits_per_step: number;
    credits_per_usd: number;
}

export interface TopupLimits {
    minCents: number;
    maxCents: number;
    stepCents: number;
    creditsPerStep: number;
}

export interface AmountInputResult {
    cents: number | null;
    error: string;
}

export interface TopupPickerProps {
    config: TopupConfig;
    onContinue: (cents: number) => void;
}

export interface TopupPresetsProps {
    presets: number[];
    selected: number;
    onPick: (cents: number) => void;
}