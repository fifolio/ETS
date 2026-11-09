import type { Models } from "appwrite";

export type AppUser = Models.User<
    Models.Preferences & {
        role?: string;
        seniority?: string;
        yearsOfExperience?: number | null;
        currentLocation?: string;
        desiredLocations?: string[];
        workArrangements?: string[];
        employmentTypes?: string[];
        willingToRelocate?: boolean;
        // hourlyRate?: number | null;
        // currency?: string;
        industryId?: string;
        industry?: string;
        jobId?: string;
        hourlyRateUsd?: number | null;
    }
>;

export type VerificationStatus = "working" | "done" | "failed";

export interface SignUpInput {
    name: string;
    email: string;
    password: string;
}

export interface LogInInput {
    email: string;
    password: string;
}

export interface ConfirmVerificationInput {
    userId: string;
    secret: string;
}