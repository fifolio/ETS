import { account } from "@/lib/appwrite";
import type { ConfirmVerificationInput } from "@/types/auth/auth";

export async function confirmVerification({
    userId,
    secret,
}: ConfirmVerificationInput): Promise<void> {
    await account.updateEmailVerification({ userId, secret });
}