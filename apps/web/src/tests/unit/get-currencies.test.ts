import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { getCurrencies } from "@/services/currencies/get-currencies";

const fetchMock = vi.fn();

beforeEach(() => { vi.stubEnv("NEXT_PUBLIC_API_URL", "http://api.test"); vi.stubGlobal("fetch", fetchMock); fetchMock.mockReset(); });
afterEach(() => { vi.unstubAllEnvs(); vi.unstubAllGlobals(); });

describe("getCurrencies", () => {
    it("loads currencies from the public endpoint", async () => {
        fetchMock.mockResolvedValue(new Response(JSON.stringify([{ code: "usd", name: "US Dollar", symbol: "$", rate_from_usd: 1 }]), { status: 200 }));
        expect(await getCurrencies()).toHaveLength(1);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/currencies");
    });
    it("throws on error", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));
        await expect(getCurrencies()).rejects.toThrow();
    });
});