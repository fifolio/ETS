import type { Industry, Job } from "@/types/catalog";
import type { JobSelection } from "@/types/profile";

/** The user's choice as it is saved in their preferences, or null if it isn't complete. */
export function buildJobSelection(
    industries: Industry[],
    jobs: Job[],
    industryId: string,
    jobId: string,
): JobSelection | null {
    const industry = industries.find((item) => item.id === industryId);
    const job = jobs.find((item) => item.id === jobId);
    if (!industry || !job) {
        return null;
    }
    return {
        industryId: industry.id,
        industry: industry.name,
        jobId: job.id,
        role: job.name,
        hourlyRateUsd: job.hourly_rate_usd,
    };
}