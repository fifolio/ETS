import { account } from "@/lib/appwrite";
import type { AppUser } from "@/types/auth/auth";

/** Returns the logged-in user, or null when there is no active session. */
export async function loadSession(): Promise<AppUser | null> {
  try {
    return await account.get();
  } catch {
    return null;
  }
}