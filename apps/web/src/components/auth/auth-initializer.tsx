"use client";

import { useEffect } from "react";

import { useAuthStore } from "@/stores/auth/auth-store";

/** Checks once, when the app loads, whether a user is already logged in. */
export function AuthInitializer() {
    const loadSession = useAuthStore((state) => state.loadSession);

    useEffect(() => {
        void loadSession();
    }, [loadSession]);

    return null;
}