import { account } from "@/lib/appwrite";

export async function changePassword(oldPassword: string, newPassword: string): Promise<void> {
    await account.updatePassword({ password: newPassword, oldPassword });
}