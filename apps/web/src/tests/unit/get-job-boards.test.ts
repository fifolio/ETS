import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getJobBoards } from "@/services/job-boards/get-job-boards";

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

describe("getJobBoards", () => {
    it("loads the full list from the public endpoint", async () => {
        const list = [{
            id: "linkedin",
            name: "LinkedIn",
            url: "https://www.linkedin.com/jobs",
            plan: "nextmove",
            plan_name: "Next Move",
        }];
        fetchMock.mockResolvedValue(new Response(JSON.stringify(list), { status: 200 }));

        expect(await getJobBoards()).toEqual(list);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/job-boards");
    });

    it("throws a readable error when the API fails", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getJobBoards()).rejects.toThrow("The API answered with status 502.");
    });

    it("throws when the API can't be reached", async () => {
        fetchMock.mockRejectedValue(new Error("offline"));

        await expect(getJobBoards()).rejects.toThrow("offline");
    });
});