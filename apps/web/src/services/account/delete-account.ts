import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";

/** Deletes the account and all of its data (the testimonial, if any, is kept). */
export async function deleteAccount(): Promise<void> {
    const response = await apiFetch("/account", { method: "DELETE" });
    if (!response.ok) {
        throw await readApiError(response);
    }
}