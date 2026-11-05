import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";

export function useVerificationPolling(enabled: boolean): void {
    const refresh = useAuthStore((state) => state.refresh);

    useEffect(() => {
        if (!enabled) {
            return;
        }
        const timer = setInterval(() => void refresh(), 5000);
        return () => clearInterval(timer);
    }, [enabled, refresh]);
}