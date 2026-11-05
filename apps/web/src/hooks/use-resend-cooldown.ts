import { useEffect, useState } from "react";

export function useResendCooldown(seconds = 60) {
    const [remaining, setRemaining] = useState(0);

    useEffect(() => {
        if (remaining <= 0) {
            return;
        }
        const timer = setTimeout(() => setRemaining(remaining - 1), 1000);
        return () => clearTimeout(timer);
    }, [remaining]);

    return { remaining, start: () => setRemaining(seconds) };
}