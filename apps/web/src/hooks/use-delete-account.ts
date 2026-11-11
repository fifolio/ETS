import { useRouter } from "next/navigation";
import { useState } from "react";

import { deleteAccount } from "@/services/account/delete-account";
import { useAuthStore } from "@/stores/auth/auth-store";

export function useDeleteAccount() {
    const router = useRouter();
    const signOutLocally = useAuthStore((state) => state.signOutLocally);
    const [confirmation, setConfirmation] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");

    async function handleDelete() {
        setBusy(true);
        setError("");
        try {
            await deleteAccount();
            signOutLocally();
            router.push("/");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not delete your account.");
            setBusy(false);
        }
    }

    return { confirmation, setConfirmation, busy, error, handleDelete };
}