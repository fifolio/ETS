import { DEFAULT_ACCOUNT_PREFS, LANGUAGES, THEMES } from "@/constants/account-defaults";
import type { AccountPrefs } from "@/types/account";
import type { AppUser } from "@/types/auth/auth";

export function readAccountPrefs(user: AppUser): AccountPrefs {
    const { theme, language } = user.prefs as {

        theme: string;
        language: string;
    };
    return {
        theme: THEMES.find((item) => item === theme) ?? DEFAULT_ACCOUNT_PREFS.theme,
        language: LANGUAGES.find((item) => item === language) ?? DEFAULT_ACCOUNT_PREFS.language,
    };
}