import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import type { SiteTotals } from "@/types/stats";

export async function getSiteTotals(): Promise<SiteTotals | null> {
    try {
        const response = await fetch(`${getApiBaseUrl()}/stats/totals`, { cache: "no-store" });
        if (!response.ok) {
            console.error(`Could not load site totals: API returned ${response.status}`);
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error("Could not load site totals:", error);
        return null;
    }
}