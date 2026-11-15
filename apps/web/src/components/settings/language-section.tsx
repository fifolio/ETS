"use client";

import { useLanguages } from "@/hooks/use-languages";
import { useSaveAccountPref } from "@/hooks/use-save-account-pref";
import { readAccountPrefs } from "@/lib/account/read-account-prefs";
import { describeLanguage } from "@/lib/language/describe-language";
import { useAuthStore } from "@/stores/auth/auth-store";

export function LanguageSection() {
    const user = useAuthStore((state) => state.user);
    const { languages, error: loadError } = useLanguages();
    const { save, busy, message, error } = useSaveAccountPref();

    if (!user) {
        return null;
    }
    const { language } = readAccountPrefs(user);

    return (
        <section>
            <h2>Language</h2>
            {loadError && <p role="alert">{loadError}</p>}
            {!languages && !loadError && <p>Loading...</p>}
            {languages && (
                <label>
                    Language{" "}
                    <select value={language} disabled={busy} onChange={(event) => save({ language: event.target.value })}>
                        {languages.map((item) => (
                            <option key={item.code} value={item.code}>
                                {describeLanguage(item)}
                            </option>
                        ))}
                    </select>
                </label>
            )}
            <p>
                This language is also used in the ETS extension. Until a language is translated, English
                is shown. The text of this website is still English only.
            </p>
            {message && <p>{message}</p>}
            {error && <p role="alert">{error}</p>}
        </section>
    );
}