import { DEFAULT_ACCOUNT_PREFS, THEMES } from "@/constants/account-defaults";
import type { AccountPrefs } from "@/types/account";
import type { AppUser } from "@/types/auth/auth";

const LANGUAGE_CODE = /^[a-z]{2,3}$/;

export function readAccountPrefs(user: AppUser): AccountPrefs {
    const { theme, language } = user.prefs;
    return {
        theme: THEMES.find((item) => item === theme) ?? DEFAULT_ACCOUNT_PREFS.theme,
        language:
            typeof language === "string" && LANGUAGE_CODE.test(language)
                ? language
                : DEFAULT_ACCOUNT_PREFS.language,
    };
}