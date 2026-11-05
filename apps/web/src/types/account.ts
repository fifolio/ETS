export type ThemePreference = "light" | "dark";
export type LanguageCode = "en" | "ar" | "fr" | "es";
export type SubscriptionPlan = "explore" | "nextmove" | "urgent";

export interface AccountPrefs {
  theme: ThemePreference;
  language: LanguageCode;
}