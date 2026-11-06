import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getPublicTestimonials } from "@/services/testimonials/get-public-testimonials";

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

describe("getPublicTestimonials", () => {
    it("returns the testimonials from the public endpoint", async () => {
        const list = [{ id: "1", quote: "Great", display_name: "Jane D.", role: null, hours_saved: 2, scans: 20 }];
        fetchMock.mockResolvedValue(new Response(JSON.stringify(list), { status: 200 }));

        expect(await getPublicTestimonials()).toEqual(list);
        expect(fetchMock.mock.calls[0][0]).toBe("http://api.test/testimonials?limit=12");
    });

    it("returns an empty list when the API answers with an error", async () => {
        fetchMock.mockResolvedValue(new Response("{}", { status: 502 }));

        expect(await getPublicTestimonials()).toEqual([]);
    });

    it("returns an empty list when the API can't be reached", async () => {
        fetchMock.mockRejectedValue(new Error("offline"));

        expect(await getPublicTestimonials()).toEqual([]);
    });
});