import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getIndustries } from "@/services/catalog/get-industries";
import { getIndustryJobs } from "@/services/catalog/get-industry-jobs";

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

describe("catalog services", () => {
    it("loads the industries from the API", async () => {
        const list = [{ id: "marketing", name: "Marketing & Advertising" }];
        fetchMock.mockResolvedValue(new Response(JSON.stringify(list), { status: 200 }));

        expect(await getIndustries()).toEqual(list);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/industries");
    });

    it("loads the roles of an industry and encodes the industry id", async () => {
        fetchMock.mockResolvedValue(new Response("[]", { status: 200 }));

        await getIndustryJobs("a b");

        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/industries/a%20b/jobs");
    });

    it("throws a readable error when the API fails", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getIndustries()).rejects.toThrow("The API answered with status 502.");
    });
});