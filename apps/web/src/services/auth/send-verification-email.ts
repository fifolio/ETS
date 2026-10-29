import { account } from "@/lib/appwrite";

export async function sendVerificationEmail(): Promise<void> {
  await account.createEmailVerification({ url: `${window.location.origin}/verify` });
}