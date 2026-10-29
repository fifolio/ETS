"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";
import type { ChildrenProps } from "@/types/common";

export function RequireAuth({ children }: ChildrenProps) {
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);
    const router = useRouter();

    useEffect(() => {
        if (!loading && !user) {
            router.replace("/login");
        }
    }, [loading, user, router]);

    if (loading || !user) {
        return <p>Loading...</p>;
    }
    return <>{children}</>;
}