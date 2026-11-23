import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { startCheckout } from "@/services/subscription/start-checkout";

const session = {
    provider: "whop",
    environment: "sandbox",
    checkout_id: "ch_1",
    plan_id: "plan_1",
    checkout_url: "https://sandbox.whop.com/checkout/plan_1/?session=ch_1",
    amount_cents: 700,
    credits: 150,
};

beforeEach(() => {
    apiFetch.mockReset();
});

describe("startCheckout", () => {
    it("asks the API for a checkout of the product and returns the session", async () => {
        apiFetch.mockResolvedValue(new Response(JSON.stringify(session), { status: 200 }));

        expect(await startCheckout("nextmove")).toEqual(session);

        const [path, init] = apiFetch.mock.calls[0];
        expect(path).toBe("/subscription/checkout");
        expect(JSON.parse(init.body)).toEqual({ product: "nextmove" });
    });

    it("throws the API's message when payments aren't available", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "Payments are not available yet." }), { status: 503 }),
        );

        await expect(startCheckout("urgent")).rejects.toThrow("Payments are not available yet.");
    });

    it("throws the API's message when the purchase isn't allowed", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "You are already on this plan." }), { status: 400 }),
        );

        await expect(startCheckout("nextmove")).rejects.toThrow("already on this plan");
    });

    it("sends the amount for a top-up", async () => {
        apiFetch.mockResolvedValue(new Response(JSON.stringify({ ...session, amount_cents: 525, credits: 42 }), { status: 200 }));

        await startCheckout("topup", 5.25);

        expect(JSON.parse(apiFetch.mock.calls[0][1].body)).toEqual({ product: "topup", amount_usd: 5.25 });
    });
});