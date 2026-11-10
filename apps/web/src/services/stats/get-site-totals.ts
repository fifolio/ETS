import { SITE_TOTALS_CACHE_SECONDS } from "@/constants/stats";
import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import type { SiteTotals } from "@/types/stats";

export async function getSiteTotals(): Promise<SiteTotals | null> {
    try {
        const response = await fetch(`${getApiBaseUrl()}/stats/totals`, {
            next: { revalidate: SITE_TOTALS_CACHE_SECONDS },
        });
        return response.ok ? await response.json() : null;
    } catch {
        return null;
    }
}