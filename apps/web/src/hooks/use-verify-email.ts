import { useEffect, useState } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";
import { confirmVerification } from "@/services/auth/confirm-verification";
import type { VerificationStatus } from "@/types/auth/auth";

export function useVerifyEmail(): VerificationStatus {
    const refresh = useAuthStore((state) => state.refresh);
    const [status, setStatus] = useState<VerificationStatus>("working");

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const userId = params.get("userId");
        const secret = params.get("secret");

        const task =
            userId && secret
                ? confirmVerification({ userId, secret })
                : Promise.reject(new Error("Missing link parameters"));

        task
            .then(() => refresh())
            .then(() => setStatus("done"))
            .catch(() => setStatus("failed"));
    }, [refresh]);

    return status;
}