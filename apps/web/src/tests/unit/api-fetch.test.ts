import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const { createJWT } = vi.hoisted(() => ({ createJWT: vi.fn() }));

vi.mock("@/lib/appwrite", () => ({ account: { createJWT } }));

import { apiFetch } from "@/lib/api/api-fetch";
import { clearApiToken } from "@/lib/api/clear-api-token";

const fetchMock = vi.fn();

beforeEach(() => {
    vi.useFakeTimers();
    vi.stubEnv("NEXT_PUBLIC_API_URL", "http://api.test");
    vi.stubGlobal("fetch", fetchMock);
    clearApiToken();
    createJWT.mockReset().mockResolvedValueOnce({ jwt: "token-1" }).mockResolvedValue({ jwt: "token-2" });
    fetchMock.mockReset().mockImplementation(async () => new Response("{}", { status: 200 }));
});

afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
});

describe("apiFetch", () => {
    it("calls the API with the user's token in the Authorization header", async () => {
        await apiFetch("/cv");

        const [url, init] = fetchMock.mock.calls[0];
        expect(url).toBe("http://api.test/cv");
        expect(new Headers(init.headers).get("Authorization")).toBe("Bearer token-1");
    });

    it("reuses one token for several requests", async () => {
        await apiFetch("/cv");
        await apiFetch("/cv");

        expect(createJWT).toHaveBeenCalledTimes(1);
    });

    it("gets a new token after 10 minutes", async () => {
        await apiFetch("/cv");
        vi.advanceTimersByTime(10 * 60 * 1000 + 1);
        await apiFetch("/cv");

        expect(createJWT).toHaveBeenCalledTimes(2);
    });

    it("gets a new token after the cache is cleared, for example on logout", async () => {
        await apiFetch("/cv");
        clearApiToken();
        await apiFetch("/cv");

        expect(createJWT).toHaveBeenCalledTimes(2);
    });

    it("retries once with a fresh token when the API answers 401", async () => {
        fetchMock.mockResolvedValueOnce(new Response("{}", { status: 401 }));

        const response = await apiFetch("/cv");

        expect(response.status).toBe(200);
        expect(fetchMock).toHaveBeenCalledTimes(2);
        expect(new Headers(fetchMock.mock.calls[1][1].headers).get("Authorization")).toBe("Bearer token-2");
    });
});