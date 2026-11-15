import type { ThemePreference } from "@/types/account";

/** Applies the theme to the document for app styles and browser controls. */
export function applyTheme(theme: ThemePreference, root: HTMLElement): void {
    root.style.colorScheme = theme;
    root.dataset.theme = theme;
}