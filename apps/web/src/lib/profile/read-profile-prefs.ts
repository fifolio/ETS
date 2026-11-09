import { EMPLOYMENT_TYPES } from "@/constants/employment-types";
import { SENIORITY_LEVELS } from "@/constants/seniority-levels";
import { WORK_ARRANGEMENTS } from "@/constants/work-arrangements";
import { pickKnown } from "@/lib/profile/pick-known";
import type { AppUser } from "@/types/auth/auth";
import type { ProfilePrefs } from "@/types/profile";

const text = (value: unknown): string => (typeof value === "string" ? value : "");
const number = (value: unknown): number | null => (typeof value === "number" ? value : null);

export function readProfilePrefs(user: AppUser): ProfilePrefs {
    const prefs = user.prefs;
    return {
        industryId: text(prefs.industryId),
        industry: text(prefs.industry),
        jobId: text(prefs.jobId),
        role: text(prefs.role),
        hourlyRateUsd: number(prefs.hourlyRateUsd),
        seniority: SENIORITY_LEVELS.find((level) => level.value === prefs.seniority)?.value ?? "",
        yearsOfExperience: number(prefs.yearsOfExperience),
        currentLocation: text(prefs.currentLocation),
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
    };
}