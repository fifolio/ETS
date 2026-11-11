"use client";

import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import { useAuthStore } from "@/stores/auth/auth-store";

export function AccountDetails() {
    const user = useAuthStore((state) => state.user);

    if (!user) {
        return null;
    }
    const { industry, role } = readProfilePrefs(user);

    return (
        <section>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
            <p>Industry: {industry || "not set"}</p>
            <p>Role: {role || "not set"}</p>
        </section>
    );
}