import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { getCredits } from "@/services/credits/get-credits";

beforeEach(() => {
    apiFetch.mockReset();
});

describe("getCredits", () => {
    it("asks the API for the balances", async () => {
        const body = { subscription: 10, promotional: 2, purchased: 5, total: 17, credits_per_scan: 1 };
        apiFetch.mockResolvedValue(new Response(JSON.stringify(body), { status: 200 }));

        expect(await getCredits()).toEqual(body);
        expect(apiFetch).toHaveBeenCalledWith("/credits");
    });

    it("throws the API's message when the user isn't verified", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "Verify your email first." }), { status: 403 }),
        );

        await expect(getCredits()).rejects.toThrow("Verify your email first.");
    });

    it("throws when the API fails", async () => {
        apiFetch.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getCredits()).rejects.toThrow("The API answered with status 502.");
    });
});