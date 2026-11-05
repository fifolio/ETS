import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { OnboardingStatus } from "@/types/onboarding/onboarding";

export async function getOnboardingStatus(): Promise<OnboardingStatus> {
    const response = await apiFetch("/onboarding/status");
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}