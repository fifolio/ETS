"use client";

import { useAuthStore } from "@/stores/auth/auth-store";
import { ResendVerificationButton } from "./resend-verification-button";
import { readAccountPrefs } from "@/lib/account/read-account-prefs";
import { readSubscription } from "@/lib/account/read-subscription";
import type { AppUser } from "@/types/auth/auth";

export function AccountDetails() {
    const user = useAuthStore((state) => state.user);
    const { theme, language } = readAccountPrefs(user as AppUser);

    if (!user) {
        return null;
    }
    return (
        <section>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
            <p>Plan: {readSubscription(user)}</p>
            <p>Theme: {theme}</p>
            <p>Language: {language}</p>
            <p>Email verified: {user.emailVerification ? "yes" : "no"}</p>
            {!user.emailVerification && <ResendVerificationButton />}
        </section>
    );
}