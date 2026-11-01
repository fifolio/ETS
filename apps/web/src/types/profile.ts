export type SeniorityLevel = "intern" | "junior" | "mid" | "senior" | "lead";

export interface SeniorityOption {
    value: SeniorityLevel;
    label: string;
}

export interface ProfilePrefs {
    role: string;
    seniority: SeniorityLevel | "";
}

export interface SetupStep {
    label: string;
    done: boolean;
}