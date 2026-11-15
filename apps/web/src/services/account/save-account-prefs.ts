import { account } from "@/lib/appwrite";
import type { AccountPrefs } from "@/types/account";
import type { AppUser } from "@/types/auth/auth";

/** Saves theme or language changes, keeping every other preference. */
export async function saveAccountPrefs(
    current: AppUser["prefs"],
    changes: Partial<AccountPrefs>,
): Promise<void> {
    await account.updatePrefs({ prefs: { ...current, ...changes } });
}