import { apiFetch } from "@/lib/api/api-fetch";

export async function checkApiConnection(): Promise<string> {
    try {
        const response = await apiFetch("/cv");
        if (response.status === 404) {
            return "API connected. You are logged in and have no CV uploaded yet.";
        }
        if (response.ok) {
            return "API connected. You already have a CV stored.";
        }
        return `The API answered with status ${response.status}.`;
    } catch {
        return "Could not reach the API. Check if it's running, and is CORS set up?";
    }
}