import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { MyJobBoards } from "@/types/job-boards";

export async function getMyJobBoards(): Promise<MyJobBoards> {
    const response = await apiFetch("/job-boards/mine");
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}