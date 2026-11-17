"use client";

import { useCurrencies } from "@/hooks/use-currencies";
import { useSaveAccountPref } from "@/hooks/use-save-account-pref";
import { useAuthStore } from "@/stores/auth/auth-store";

export function CurrencySection() {
    const user = useAuthStore((state) => state.user);
    const { currencies, error: loadError } = useCurrencies();
    const { save, busy, message, error } = useSaveAccountPref();

    if (!user) return null;

    const prefs = user.prefs as Record<string, unknown>;
    const saved = typeof prefs.currency === "string" ? prefs.currency : "usd";

    return (
        <section>
            <h2>Currency</h2>
            {loadError && <p role="alert">{loadError}</p>}
            {!currencies && !loadError && <p>Loading...</p>}
            {currencies && (
                <label>
                    Display currency{" "}
                    <select value={saved} disabled={busy} onChange={(e) => save({ currency: e.target.value } as never)}>
                        {currencies.map((c) => (
                            <option key={c.code} value={c.code}>
                                {c.symbol} {c.name} ({c.code.toUpperCase()})
                            </option>
                        ))}
                    </select>
                </label>
            )}
            <p>Cash saved figures are converted from USD using stored rates. Rates are approximate.</p>
            {message && <p>{message}</p>}
            {error && <p role="alert">{error}</p>}
        </section>
    );
}