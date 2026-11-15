export type ThemePreference = "light" | "dark";
export type LanguageCode = string;
export type SubscriptionPlan = "explore" | "nextmove" | "urgent";

export interface AccountPrefs {
  theme: ThemePreference;
  language: LanguageCode;
}