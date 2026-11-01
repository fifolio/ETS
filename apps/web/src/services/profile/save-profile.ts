import { account } from "@/lib/appwrite";
import type { AppUser } from "@/types/auth/auth";
import type { ProfilePrefs } from "@/types/profile";

/** Saves the role and seniority, keeping any other preferences already stored. */
export async function saveProfile(current: AppUser["prefs"], profile: ProfilePrefs): Promise<void> {
    await account.updatePrefs({ prefs: { ...current, ...profile } });
}