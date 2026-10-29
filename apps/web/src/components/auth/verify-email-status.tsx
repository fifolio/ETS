"use client";

import Link from "next/link";

import { useVerifyEmail } from "@/hooks/use-verify-email";

export function VerifyEmailStatus() {
    const status = useVerifyEmail();

    if (status === "working") {
        return <p>Verifying...</p>;
    }
    if (status === "done") {
        return (
            <p>
                Your email is verified. <Link href="/profile">Go to your profile</Link>
            </p>
        );
    }
    return (
        <p role="alert">
            This link is invalid or expired, or you are not logged in. Log in, then request a new email
            from your <Link href="/profile">profile</Link>.
        </p>
    );
}