export type SeniorityLevel = "intern" | "junior" | "mid" | "senior" | "lead";
export type WorkArrangement = "remote" | "hybrid" | "onsite";
export type EmploymentType = "full-time" | "part-time" | "contract" | "internship" | "freelance";

export interface OptionItem<T extends string> {
  value: T;
  label: string;
}

/** The industry and role the user picked, with the role's hourly rate. */
export interface JobSelection {
  industryId: string;
  industry: string;
  jobId: string;
  role: string;
  hourlyRateUsd: number | null;
}

export interface ProfileAnswers {
  seniority: SeniorityLevel | "";
  yearsOfExperience: number | null;
  currentLocation: string;
  desiredLocations: string[];
  workArrangements: WorkArrangement[];
  employmentTypes: EmploymentType[];
  willingToRelocate: boolean;
}

export type ProfilePrefs = JobSelection & ProfileAnswers;