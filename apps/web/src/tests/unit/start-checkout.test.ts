import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { startCheckout } from "@/services/subscription/start-checkout";

beforeEach(() => {
    apiFetch.mockReset();
});

describe("startCheckout", () => {
    it("asks the API for a checkout of the plan and returns the payment page address", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ checkout_url: "https://pay.example/1" }), { status: 200 }),
        );

        expect(await startCheckout("nextmove")).toBe("https://pay.example/1");

        const [path, init] = apiFetch.mock.calls[0];
        expect(path).toBe("/subscription/checkout");
        expect(JSON.parse(init.body)).toEqual({ plan: "nextmove" });
    });

    it("throws the API's message when payments aren't available", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "Payments are not available yet." }), { status: 503 }),
        );

        await expect(startCheckout("urgent")).rejects.toThrow("Payments are not available yet.");
    });

    it("throws the API's message when the plan can't be chosen", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "You are already on this plan." }), { status: 400 }),
        );

        await expect(startCheckout("nextmove")).rejects.toThrow("already on this plan");
    });
});