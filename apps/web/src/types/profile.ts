export type SeniorityLevel = "intern" | "junior" | "mid" | "senior" | "lead";
export type WorkArrangement = "remote" | "hybrid" | "onsite";
export type EmploymentType = "full-time" | "part-time" | "contract" | "internship" | "freelance";

export interface OptionItem<T extends string> {
    value: T;
    label: string;
}

export interface ProfilePrefs {
    role: string;
    seniority: SeniorityLevel | "";
    yearsOfExperience: number | null;
    currentLocation: string;
    desiredLocations: string[];
    workArrangements: WorkArrangement[];
    employmentTypes: EmploymentType[];
    willingToRelocate: boolean;
    hourlyRate: number | null;
    currency: string;
}