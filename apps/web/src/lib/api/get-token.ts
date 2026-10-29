import { account } from "@/lib/appwrite";
import { TOKEN_LIFETIME_MS, tokenCache } from "@/lib/api/token-cache";


export async function getToken(): Promise<string> {
    const cached = tokenCache.current;
    if (cached && Date.now() < cached.expiresAt) {
        return cached.token;
    }
    const { jwt } = await account.createJWT();
    tokenCache.current = { token: jwt, expiresAt: Date.now() + TOKEN_LIFETIME_MS };
    return jwt;
}