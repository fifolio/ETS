"use client";

import type { ReactNode } from "react";

import { AccountDetails } from "@/components/dashboard/account-details";
import { CvSection } from "@/components/cv/cv-section";
import { ProfileForm } from "@/components/profile/profile-form";
import { useAuthStore } from "@/stores/auth/auth-store";

interface AuthAwareHomeProps {
    publicContent: ReactNode;
}

export function AuthAwareHome({ publicContent }: AuthAwareHomeProps) {
    const user = useAuthStore((state) => state.user);
    const loading = useAuthStore((state) => state.loading);

    if (loading || !user) {
        return <>{publicContent}</>;
    }

    return (
        <main>
            <h1>Dashboard</h1>
            <AccountDetails />
            <ProfileForm />
            <CvSection />
        </main>
    );
}
