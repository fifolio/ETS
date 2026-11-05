import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { getOnboardingRedirect } from "@/lib/onboarding/get-onboarding-redirect";
import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function useOnboardingRedirect(): void {
    const router = useRouter();
    const pathname = usePathname();
    const user = useAuthStore((state) => state.user);
    const status = useOnboardingStore((state) => state.status);

    useEffect(() => {
        if (!user || !status) {
            return;
        }
        const target = getOnboardingRedirect(pathname, true, status.complete);
        if (target) {
            router.replace(target);
        }
    }, [user, status, pathname, router]);
}