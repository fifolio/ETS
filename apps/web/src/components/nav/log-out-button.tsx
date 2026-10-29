"use client";

import { useRouter } from "next/navigation";

import { useAuthStore } from "@/stores/auth/auth-store";

export function LogOutButton() {
    const router = useRouter();
    const logOut = useAuthStore((state) => state.logOut);

    async function handleClick() {
        await logOut();
        router.push("/login");
    }

    return (
        <button type="button" onClick={handleClick}>
            Log out
        </button>
    );
}