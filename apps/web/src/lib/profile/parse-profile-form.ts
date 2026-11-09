import { parseOptionalNumber } from "@/lib/profile/parse-optional-number";
import { splitList } from "@/lib/profile/split-list";
import type {
    EmploymentType,
    ProfileAnswers,
    SeniorityLevel,
    WorkArrangement,
} from "@/types/profile";

export function parseProfileForm(data: FormData): ProfileAnswers {
    return {
        seniority: String(data.get("seniority") ?? "") as SeniorityLevel | "",
        yearsOfExperience: parseOptionalNumber(String(data.get("yearsOfExperience") ?? "")),
        currentLocation: String(data.get("currentLocation") ?? "").trim(),
        desiredLocations: splitList(String(data.get("desiredLocations") ?? "")),
        workArrangements: data.getAll("workArrangements").map(String) as WorkArrangement[],
        employmentTypes: data.getAll("employmentTypes").map(String) as EmploymentType[],
        willingToRelocate: data.get("willingToRelocate") === "on",
    };
}