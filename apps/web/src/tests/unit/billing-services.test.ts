import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { cancelSubscription } from "@/services/billing/cancel-subscription";
import { getCreditHistory } from "@/services/billing/get-credit-history";
import { getManageUrl } from "@/services/billing/get-manage-url";
import { getPaymentHistory } from "@/services/billing/get-payment-history";
import { getSubscriptionStatus } from "@/services/billing/get-subscription-status";

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status });

beforeEach(() => {
  apiFetch.mockReset();
});

describe("getSubscriptionStatus", () => {
  it("asks the API for the subscription", async () => {
    apiFetch.mockResolvedValue(json({ plan: "explore" }));

    expect(await getSubscriptionStatus()).toEqual({ plan: "explore" });
    expect(apiFetch).toHaveBeenCalledWith("/subscription");
  });

  it("throws the API's message", async () => {
    apiFetch.mockResolvedValue(json({ detail: "Verify your email first." }, 403));

    await expect(getSubscriptionStatus()).rejects.toThrow("Verify your email first.");
  });
});

describe("cancelSubscription", () => {
  it("posts the cancellation and returns the new state", async () => {
    apiFetch.mockResolvedValue(json({ cancel_at_period_end: true }));

    expect(await cancelSubscription()).toEqual({ cancel_at_period_end: true });
    expect(apiFetch).toHaveBeenCalledWith("/subscription/cancel", { method: "POST" });
  });

  it("throws the API's message when there is nothing to cancel", async () => {
    apiFetch.mockResolvedValue(json({ detail: "You have no paid subscription to cancel." }, 400));

    await expect(cancelSubscription()).rejects.toThrow("no paid subscription");
  });

  it("throws the API's message when the payment service fails", async () => {
    apiFetch.mockResolvedValue(json({ detail: "The payment service failed. Please try again." }, 502));

    await expect(cancelSubscription()).rejects.toThrow("payment service failed");
  });
});

describe("getManageUrl", () => {
  it("returns the billing page address", async () => {
    apiFetch.mockResolvedValue(json({ url: "https://whop.com/billing/manage/mem_1" }));

    expect(await getManageUrl()).toBe("https://whop.com/billing/manage/mem_1");
    expect(apiFetch).toHaveBeenCalledWith("/subscription/manage-url");
  });

  it("throws the API's message when there is no billing page", async () => {
    apiFetch.mockResolvedValue(json({ detail: "You have no paid subscription." }, 404));

    await expect(getManageUrl()).rejects.toThrow("no paid subscription");
  });

  it("throws when the API fails", async () => {
    apiFetch.mockResolvedValue(new Response("{}", { status: 502 }));

    await expect(getManageUrl()).rejects.toThrow("The API answered with status 502.");
  });
});

describe("getCreditHistory", () => {
  it("asks the API for the credit history", async () => {
    apiFetch.mockResolvedValue(json([{ amount: -1, kind: "subscription", reason: "Job scan", created_at: null }]));

    expect(await getCreditHistory()).toHaveLength(1);
    expect(apiFetch).toHaveBeenCalledWith("/credits/history");
  });

  it("throws the API's message", async () => {
    apiFetch.mockResolvedValue(json({ detail: "Verify your email first." }, 403));

    await expect(getCreditHistory()).rejects.toThrow("Verify your email first.");
  });
});

describe("getPaymentHistory", () => {
  it("asks the API for the payments", async () => {
    apiFetch.mockResolvedValue(json([]));

    expect(await getPaymentHistory()).toEqual([]);
    expect(apiFetch).toHaveBeenCalledWith("/payments");
  });

  it("throws the API's message", async () => {
    apiFetch.mockResolvedValue(json({ detail: "Verify your email first." }, 403));

    await expect(getPaymentHistory()).rejects.toThrow("Verify your email first.");
  });
});