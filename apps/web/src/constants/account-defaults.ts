import type {
    AccountPrefs,
    LanguageCode,
    SubscriptionPlan,
    ThemePreference,
} from "@/types/account";

export const THEMES: ThemePreference[] = ["light", "dark"];
export const LANGUAGES: LanguageCode[] = ["en", "ar", "fr", "es"];
export const SUBSCRIPTION_PLANS: SubscriptionPlan[] = ["explore", "nextmove", "urgent"];

// Set automatically at sign-up; the user is never asked for these.
export const DEFAULT_ACCOUNT_PREFS: AccountPrefs = { theme: "light", language: "en" };

// Keep in sync with SETUP_DEADLINE_HOURS in the API settings.
export const SETUP_DEADLINE_HOURS = 48;