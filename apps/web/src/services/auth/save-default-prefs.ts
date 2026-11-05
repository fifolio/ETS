import { DEFAULT_ACCOUNT_PREFS } from "@/constants/account-defaults";
import { account } from "@/lib/appwrite";

export async function saveDefaultPrefs(): Promise<void> {
    await account.updatePrefs({ prefs: DEFAULT_ACCOUNT_PREFS });
}