import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";

export async function deleteCv(): Promise<void> {
    const response = await apiFetch("/cv", { method: "DELETE" });
    if (!response.ok && response.status !== 404) {
        throw await readApiError(response);
    }
}