import { ID } from "appwrite";

import { account } from "@/lib/appwrite";
import { sendVerificationEmail } from "@/services/auth/send-verification-email";
import type { AppUser, SignUpInput } from "@/types/auth/auth";
import { saveDefaultPrefs } from "@/services/auth/save-default-prefs";


export async function signUp({ name, email, password }: SignUpInput): Promise<AppUser> {
    await account.create({ userId: ID.unique(), email, password, name });
    await account.createEmailPasswordSession({ email, password });
    try {
        await saveDefaultPrefs();
    } catch {
        // Not critical: the defaults are applied when the preferences are read anyway.
    }
    try {
        await sendVerificationEmail();
    } catch {
        // The account exists; the user can request the email again from the profile page.
    }
    return account.get();
}