import type { CachedToken } from "@/types/api";

// An Appwrite JWT lives 15 minutes and creating one is limited to 100 per hour,
// so one token is reused for 10 minutes.
export const TOKEN_LIFETIME_MS = 10 * 60 * 1000;

export const tokenCache: { current: CachedToken | null } = { current: null };