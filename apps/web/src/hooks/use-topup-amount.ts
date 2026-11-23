import { useState } from "react";

import { applyTextInput } from "@/lib/topup/apply-text-input";
import { creditsForCents } from "@/lib/topup/credits-for-cents";
import { snapCents } from "@/lib/topup/snap-cents";
import type { TopupLimits } from "@/types/topup";

const DEFAULT_CENTS = 500; // the slider's range starts at the minimum, but $5 is selected

const toText = (cents: number) => (cents / 100).toFixed(2);

export function useTopupAmount(limits: TopupLimits) {
    const [cents, setCents] = useState(() => snapCents(DEFAULT_CENTS, limits));
    const [text, setText] = useState(() => toText(snapCents(DEFAULT_CENTS, limits)));
    const [error, setError] = useState("");

    function setFromSlider(value: number) {
        const snapped = snapCents(value, limits);
        setCents(snapped);
        setText(toText(snapped));
        setError("");
    }

    function setFromText(value: string) {
        setText(value);
        const result = applyTextInput(value, limits);
        if (result.cents === null) {
            setError(result.error);
            return;
        }
        setCents(result.cents);
        setError("");
    }

    function commitText() {
        if (!error) {
            setText(toText(cents));
        }
    }

    return { cents, text, error, credits: creditsForCents(cents, limits), setFromSlider, setFromText, commitText };
}