import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { deleteAccount } from "@/services/account/delete-account";

beforeEach(() => {
    apiFetch.mockReset();
});

describe("deleteAccount", () => {
    it("sends a DELETE request to /account", async () => {
        apiFetch.mockResolvedValue(new Response(null, { status: 204 }));

        await deleteAccount();

        expect(apiFetch).toHaveBeenCalledWith("/account", { method: "DELETE" });
    });

    it("throws the API's message when the deletion fails", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "The storage service failed." }), { status: 502 }),
        );

        await expect(deleteAccount()).rejects.toThrow("The storage service failed.");
    });
});