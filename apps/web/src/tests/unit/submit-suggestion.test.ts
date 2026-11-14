import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));

import { submitSuggestion } from "@/services/suggestions/submit-suggestion";

const input = {
    name: "Wellfound",
    url: "https://wellfound.com/jobs",
    example_url: null,
    country: null,
    notes: null,
};

beforeEach(() => {
    apiFetch.mockReset();
});

describe("submitSuggestion", () => {
    it("posts the suggestion and returns the receipt", async () => {
        const receipt = { status: "pending", remaining_today: 2 };
        apiFetch.mockResolvedValue(new Response(JSON.stringify(receipt), { status: 201 }));

        expect(await submitSuggestion(input)).toEqual(receipt);

        const [path, init] = apiFetch.mock.calls[0];
        expect(path).toBe("/job-board-suggestions");
        expect(init.method).toBe("POST");
        expect(JSON.parse(init.body)).toEqual(input);
    });

    it("throws the API's message when the board is already supported", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "LinkedIn is already supported." }), { status: 409 }),
        );

        await expect(submitSuggestion(input)).rejects.toThrow("LinkedIn is already supported.");
    });

    it("throws the API's message when the daily limit is reached", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "You reached today's limit." }), { status: 429 }),
        );

        await expect(submitSuggestion(input)).rejects.toThrow("You reached today's limit.");
    });
});