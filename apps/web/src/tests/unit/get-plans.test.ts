import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getPlans } from "@/services/plans/get-plans";

const fetchMock = vi.fn();

beforeEach(() => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "http://api.test");
    vi.stubGlobal("fetch", fetchMock);
    fetchMock.mockReset();
});

afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
});

describe("getPlans", () => {
    it("loads the plans from the public endpoint", async () => {
        const body = { plans: [], payments_enabled: false };
        fetchMock.mockResolvedValue(new Response(JSON.stringify(body), { status: 200 }));

        expect(await getPlans()).toEqual(body);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/plans");
    });

    it("throws a readable error when the API fails", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getPlans()).rejects.toThrow("The API answered with status 502.");
    });

    it("throws when the API can't be reached", async () => {
        fetchMock.mockRejectedValue(new Error("offline"));

        await expect(getPlans()).rejects.toThrow("offline");
    });
});