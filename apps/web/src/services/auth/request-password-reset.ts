import { account } from "@/lib/appwrite";

/** Sends a recovery email. The link in the email points to /reset-password. */
export async function requestPasswordReset(email: string): Promise<void> {
    const url = `${window.location.origin}/reset-password`;
    await account.createRecovery({ email, url });
}