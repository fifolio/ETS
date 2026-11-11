"use client";

import { useAuthStore } from "@/stores/auth/auth-store";

import { ResendVerificationButton } from "./resend-verification-button";

export function AccountSection() {
    const user = useAuthStore((state) => state.user);

    if (!user) {
        return null;
    }
    return (
        <section>
            <h2>Account</h2>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
            <p>Email verification: {user.emailVerification ? "Verified" : "Not verified"}</p>
            {!user.emailVerification && <ResendVerificationButton />}
        </section>
    );
}