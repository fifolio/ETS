"use client";

import { useEffect } from "react";

import { DEFAULT_ACCOUNT_PREFS } from "@/constants/account-defaults";
import { readAccountPrefs } from "@/lib/account/read-account-prefs";
import { applyTheme } from "@/lib/theme/apply-theme";
import { useAuthStore } from "@/stores/auth/auth-store";

/** Applies the saved theme to the page. Logged-out visitors get the default (light). */
export function AppearanceApplier() {
    const theme = useAuthStore((state) =>
        state.user ? readAccountPrefs(state.user).theme : DEFAULT_ACCOUNT_PREFS.theme,
    );

    useEffect(() => {
        applyTheme(theme, document.documentElement);
    }, [theme]);

    return null;
}