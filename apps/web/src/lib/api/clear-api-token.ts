import { tokenCache } from "@/lib/api/token-cache";

export function clearApiToken(): void {
    tokenCache.current = null;
}