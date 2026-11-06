import { beforeEach, describe, expect, it, vi } from "vitest";

const services = vi.hoisted(() => ({ check: vi.fn(), submit: vi.fn() }));

vi.mock("@/services/feedback/check-feedback-eligibility", () => ({
    checkFeedbackEligibility: services.check,
}));
vi.mock("@/services/feedback/submit-feedback", () => ({ submitFeedback: services.submit }));

import { ApiRequestError } from "@/lib/api/api-request-error";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";

const input = { quote: "Great", internal_suggestions: "", consent: true };

beforeEach(() => {
    vi.resetAllMocks();
    useFeedbackStore.setState({ eligible: false, submitted: false, dismissed: false });
});

describe("feedback store", () => {
    it("becomes eligible when the API says so", async () => {
        services.check.mockResolvedValue({ eligible: true });

        await useFeedbackStore.getState().check();

        expect(useFeedbackStore.getState().eligible).toBe(true);
    });

    it("stays quiet when the eligibility check fails", async () => {
        services.check.mockRejectedValue(new Error("API down"));

        await useFeedbackStore.getState().check();

        expect(useFeedbackStore.getState().eligible).toBe(false);
    });

    it("hides the form when dismissed", () => {
        useFeedbackStore.getState().dismiss();

        expect(useFeedbackStore.getState().dismissed).toBe(true);
    });

    it("marks the feedback as submitted and not eligible anymore", async () => {
        useFeedbackStore.setState({ eligible: true });
        services.submit.mockResolvedValue(undefined);

        await useFeedbackStore.getState().submit(input);

        expect(useFeedbackStore.getState()).toMatchObject({ submitted: true, eligible: false });
    });

    it("treats a 409 as already sent, without an error", async () => {
        useFeedbackStore.setState({ eligible: true });
        services.submit.mockRejectedValue(new ApiRequestError(409, "Already sent"));

        await useFeedbackStore.getState().submit(input);

        expect(useFeedbackStore.getState()).toMatchObject({ submitted: false, eligible: false });
    });

    it("passes any other error on", async () => {
        services.submit.mockRejectedValue(new ApiRequestError(502, "Storage failed"));

        await expect(useFeedbackStore.getState().submit(input)).rejects.toThrow("Storage failed");
    });
});