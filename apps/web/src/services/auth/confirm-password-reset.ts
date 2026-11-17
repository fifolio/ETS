import { account } from "@/lib/appwrite";

export async function confirmPasswordReset(
    userId: string,
    secret: string,
    password: string,
): Promise<void> {
    await account.updateRecovery({ userId, secret, password });
}