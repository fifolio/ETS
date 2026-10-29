import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";

export function useRedirectIfLoggedIn(to: string): void {
    const router = useRouter();
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);

    useEffect(() => {
        if (!loading && user) {
            router.replace(to);
        }
    }, [loading, user, router, to]);
}