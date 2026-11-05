import { CURRENCIES, DEFAULT_CURRENCY } from "@/constants/currencies";
import { EMPLOYMENT_TYPES } from "@/constants/employment-types";
import { SENIORITY_LEVELS } from "@/constants/seniority-levels";
import { WORK_ARRANGEMENTS } from "@/constants/work-arrangements";
import { pickKnown } from "@/lib/profile/pick-known";
import type { AppUser } from "@/types/auth/auth";
import type { ProfilePrefs } from "@/types/profile";

export function readProfilePrefs(user: AppUser): ProfilePrefs {
    const prefs = user.prefs;
    return {
        role: typeof prefs.role === "string" ? prefs.role : "",
        seniority: SENIORITY_LEVELS.find((level) => level.value === prefs.seniority)?.value ?? "",
        yearsOfExperience: typeof prefs.yearsOfExperience === "number" ? prefs.yearsOfExperience : null,
        currentLocation: typeof prefs.currentLocation === "string" ? prefs.currentLocation : "",
        desiredLocations: Array.isArray(prefs.desiredLocations)
            ? prefs.desiredLocations.filter((item: unknown): item is string => typeof item === "string")
            : [],
        workArrangements: pickKnown(
            prefs.workArrangements,
            WORK_ARRANGEMENTS.map((option) => option.value),
        ),
        employmentTypes: pickKnown(
            prefs.employmentTypes,
            EMPLOYMENT_TYPES.map((option) => option.value),
        ),
        willingToRelocate: prefs.willingToRelocate === true,
        hourlyRate: typeof prefs.hourlyRate === "number" ? prefs.hourlyRate : null,
        currency: CURRENCIES.includes(prefs.currency as string) ? `${prefs.currency}` : DEFAULT_CURRENCY,
    };
}