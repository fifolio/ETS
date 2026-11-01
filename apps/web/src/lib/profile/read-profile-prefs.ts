import { SENIORITY_LEVELS } from "@/constants/seniority-levels";
import type { AppUser } from "@/types/auth/auth";
import type { ProfilePrefs } from "@/types/profile";

type UserPrefs = {
    role?: string;
    seniority?: string;
};

export function readProfilePrefs(user: AppUser): ProfilePrefs {
    const { role, seniority } = user.prefs as UserPrefs;
    return {
        role: typeof role === "string" ? role : "",
        seniority: SENIORITY_LEVELS.find((level) => level.value === seniority)?.value ?? "",
    };
}