import { useEffect, useState } from "react";

import { getPlans } from "@/services/plans/get-plans";
import type { PlansResponse } from "@/types/plans";

export function usePlans() {
    const [data, setData] = useState<PlansResponse | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        getPlans()
            .then(setData)
            .catch(() => setError("Could not load the plans."));
    }, []);

    return { plans: data?.plans ?? [], paymentsEnabled: data?.payments_enabled ?? false, error, loaded: data !== null };
}