import { useEffect } from "react";

import { EXTENSION_POLL_MS } from "@/constants/extension";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function useExtensionPolling(enabled: boolean): void {
    const load = useOnboardingStore((state) => state.load);

    useEffect(() => {
        if (!enabled) {
            return;
        }
        const timer = setInterval(() => void load(), EXTENSION_POLL_MS);
        return () => clearInterval(timer);
    }, [enabled, load]);
}