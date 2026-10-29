"use client";

import { useAuthStore } from "@/stores/auth/auth-store";

import { ResendVerificationButton } from "./resend-verification-button";

export function AccountDetails() {
    const user = useAuthStore((state) => state.user);

    if (!user) {
        return null;
    }
    return (
        <section>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
            <p>Email verified: {user.emailVerification ? "yes" : "no"}</p>
            {!user.emailVerification && <ResendVerificationButton />}
        </section>
    );
}