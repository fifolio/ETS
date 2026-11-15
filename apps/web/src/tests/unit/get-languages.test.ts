import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getLanguages } from "@/services/languages/get-languages";

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

describe("getLanguages", () => {
    it("loads the languages from the public endpoint", async () => {
        const list = [{ code: "en", name: "English", native_name: "English", direction: "ltr", translated: true }];
        fetchMock.mockResolvedValue(new Response(JSON.stringify(list), { status: 200 }));

        expect(await getLanguages()).toEqual(list);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/languages");
    });

    it("throws a readable error when the API fails", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getLanguages()).rejects.toThrow("The API answered with status 502.");
    });

    it("throws when the API can't be reached", async () => {
        fetchMock.mockRejectedValue(new Error("offline"));

        await expect(getLanguages()).rejects.toThrow("offline");
    });
});