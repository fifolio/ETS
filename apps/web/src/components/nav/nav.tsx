"use client";

import { useAuthStore } from "@/stores/auth/auth-store";

import { LoggedInLinks } from "./logged-in-links";
import { LoggedOutLinks } from "./logged-out-links";

export function Nav() {
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);

    if (loading) {
        return <nav>ETS</nav>;
    }
    return <nav>{user ? <LoggedInLinks name={user.name} /> : <LoggedOutLinks />}</nav>;
}