import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function useRedirectIfLoggedIn(): void {
    const router = useRouter();
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);
    const status = useOnboardingStore((state) => state.status);

    useEffect(() => {
        if (!loading && user && status) {
            router.replace(status.complete ? "/" : "/setup");
        }
    }, [loading, user, status, router]);
}