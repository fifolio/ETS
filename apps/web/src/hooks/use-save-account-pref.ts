import { useState } from "react";

import { saveAccountPrefs } from "@/services/account/save-account-prefs";
import { useAuthStore } from "@/stores/auth/auth-store";
import type { AccountPrefs } from "@/types/account";

export function useSaveAccountPref() {
    const user = useAuthStore((state) => state.user);
    const refresh = useAuthStore((state) => state.refresh);
    const [busy, setBusy] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    async function save(changes: Partial<AccountPrefs>) {
        if (!user) {
            return;
        }
        setBusy(true);
        setMessage("");
        setError("");
        try {
            await saveAccountPrefs(user.prefs, changes);
            await refresh();
            setMessage("Saved.");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not save your choice.");
        } finally {
            setBusy(false);
        }
    }

    return { save, busy, message, error };
}