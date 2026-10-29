import { clearApiToken } from "@/lib/api/clear-api-token";
import { account } from "@/lib/appwrite";

export async function logOut(): Promise<void> {
    clearApiToken();
    await account.deleteSession({ sessionId: "current" });
}