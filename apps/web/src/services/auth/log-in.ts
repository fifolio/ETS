import { account } from "@/lib/appwrite";
import type { AppUser, LogInInput } from "@/types/auth/auth";

export async function logIn({ email, password }: LogInInput): Promise<AppUser> {
    await account.createEmailPasswordSession({ email, password });
    return account.get();
}