import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { InstalledExtension } from "@/types/extension";

export async function getExtensions(): Promise<InstalledExtension[]> {
    const response = await apiFetch("/extensions");
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}