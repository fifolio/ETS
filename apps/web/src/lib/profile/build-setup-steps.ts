import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import type { AppUser } from "@/types/auth/auth";
import type { SetupStep } from "@/types/profile";

export function buildSetupSteps(user: AppUser, hasCv: boolean): SetupStep[] {
    const prefs = readProfilePrefs(user);
    return [
        { label: "Verify your email", done: user.emailVerification },
        { label: "Set your target role and seniority", done: Boolean(prefs.role && prefs.seniority) },
        { label: "Upload your CV", done: hasCv },
    ];
}