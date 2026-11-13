import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { JobBoard } from "@/types/job-boards";

export async function getJobBoards(): Promise<JobBoard[]> {
  const response = await fetch(`${getApiBaseUrl()}/job-boards`);
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}