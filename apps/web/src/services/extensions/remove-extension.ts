import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";

export async function removeExtension(id: string): Promise<void> {
    const response = await apiFetch(`/extensions/${encodeURIComponent(id)}`, { method: "DELETE" });
    if (!response.ok && response.status !== 404) {
        throw await readApiError(response);
    }
}