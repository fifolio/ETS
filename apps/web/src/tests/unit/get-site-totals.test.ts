import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getSiteTotals } from "@/services/stats/get-site-totals";

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

describe("getSiteTotals", () => {
    it("returns the totals from the public endpoint", async () => {
        const totals = {
            total_users: 12,
            total_scans: 340,
            total_minutes_saved: 1500,
            total_hours_saved: 25,
            total_cash_saved_usd: 1250.5,
        };
        fetchMock.mockResolvedValue(new Response(JSON.stringify(totals), { status: 200 }));

        expect(await getSiteTotals()).toEqual(totals);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/stats/totals");
    });

    it("returns null when the API answers with an error", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        expect(await getSiteTotals()).toBeNull();
    });

    it("returns null when the API can't be reached", async () => {
        fetchMock.mockRejectedValue(new Error("offline"));

        expect(await getSiteTotals()).toBeNull();
    });
});