import { PAGES_OPEN_DURING_SETUP } from "@/constants/onboarding";

/** Where a visitor should be sent, or null if they can stay on the current page. */
export function getOnboardingRedirect(
    pathname: string,
    isLoggedIn: boolean,
    setupComplete: boolean,
): string | null {
    if (!isLoggedIn) {
        return null;
    }
    if (!setupComplete) {
        return PAGES_OPEN_DURING_SETUP.includes(pathname) ? null : "/setup";
    }
    return pathname === "/setup" ? "/dashboard" : null;
}