import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { getMyJobBoards } from "@/services/job-boards/get-my-job-boards";

beforeEach(() => {
    apiFetch.mockReset();
});

describe("getMyJobBoards", () => {
    it("asks the API for the user's active job boards", async () => {
        const body = { boards: [], plan: "nextmove" };
        apiFetch.mockResolvedValue(new Response(JSON.stringify(body), { status: 200 }));

        expect(await getMyJobBoards()).toEqual(body);
        expect(apiFetch).toHaveBeenCalledWith("/job-boards/mine");
    });

    it("throws the API's message when the user isn't verified", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "Verify your email first." }), { status: 403 }),
        );

        await expect(getMyJobBoards()).rejects.toThrow("Verify your email first.");
    });

    it("throws when the API fails", async () => {
        apiFetch.mockResolvedValue(new Response("{}", { status: 502 }));

        await expect(getMyJobBoards()).rejects.toThrow("The API answered with status 502.");
    });
});