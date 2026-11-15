"use client";

import { THEMES } from "@/constants/account-defaults";
import { THEME_LABELS } from "@/constants/theme-labels";
import { useSaveAccountPref } from "@/hooks/use-save-account-pref";
import { readAccountPrefs } from "@/lib/account/read-account-prefs";
import { useAuthStore } from "@/stores/auth/auth-store";

export function AppearanceSection() {
    const user = useAuthStore((state) => state.user);
    const { save, busy, message, error } = useSaveAccountPref();

    if (!user) {
        return null;
    }
    const { theme } = readAccountPrefs(user);

    return (
        <section>
            <h2>Appearance</h2>
            <fieldset disabled={busy}>
                <legend>Theme</legend>
                {THEMES.map((option) => (
                    <label key={option}>
                        <input
                            type="radio"
                            name="theme"
                            value={option}
                            checked={theme === option}
                            onChange={() => save({ theme: option })}
                        />{" "}
                        {THEME_LABELS[option]}{" "}
                    </label>
                ))}
            </fieldset>
            <p>This theme also applies to the ETS extension.</p>
            {message && <p>{message}</p>}
            {error && <p role="alert">{error}</p>}
        </section>
    );
}