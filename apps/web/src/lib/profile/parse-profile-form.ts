import { DEFAULT_CURRENCY } from "@/constants/currencies";
import { parseOptionalNumber } from "@/lib/profile/parse-optional-number";
import { splitList } from "@/lib/profile/split-list";
import type {
    EmploymentType,
    ProfilePrefs,
    SeniorityLevel,
    WorkArrangement,
} from "@/types/profile";

export function parseProfileForm(data: FormData): ProfilePrefs {
    return {
        role: String(data.get("role") ?? "").trim(),
        seniority: String(data.get("seniority") ?? "") as SeniorityLevel | "",
        yearsOfExperience: parseOptionalNumber(String(data.get("yearsOfExperience") ?? "")),
        currentLocation: String(data.get("currentLocation") ?? "").trim(),
        desiredLocations: splitList(String(data.get("desiredLocations") ?? "")),
        workArrangements: data.getAll("workArrangements").map(String) as WorkArrangement[],
        employmentTypes: data.getAll("employmentTypes").map(String) as EmploymentType[],
        willingToRelocate: data.get("willingToRelocate") === "on",
        hourlyRate: parseOptionalNumber(String(data.get("hourlyRate") ?? "")),
        currency: String(data.get("currency") ?? DEFAULT_CURRENCY),
    };
}