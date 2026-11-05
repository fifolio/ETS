import { beforeEach, describe, expect, it, vi } from "vitest";

const { getOnboardingStatus } = vi.hoisted(() => ({ getOnboardingStatus: vi.fn() }));

vi.mock("@/services/onboarding/get-onboarding-status", () => ({ getOnboardingStatus }));

import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";
import type { OnboardingStatus } from "@/types/onboarding/onboarding";

const status: OnboardingStatus = {
    steps: { verify: true, cv: false, profile: false },
    next_step: "cv",
    complete: false,
    missing_profile_fields: ["role"],
};

beforeEach(() => {
    vi.resetAllMocks();
    useOnboardingStore.setState({ status: null, error: "" });
});

describe("onboarding store", () => {
    it("stores the status from the API", async () => {
        getOnboardingStatus.mockResolvedValue(status);

        await useOnboardingStore.getState().load();

        expect(useOnboardingStore.getState()).toMatchObject({ status, error: "" });
    });

    it("keeps the error message when the API can't be reached", async () => {
        getOnboardingStatus.mockRejectedValue(new Error("Could not reach the API"));

        await useOnboardingStore.getState().load();

        expect(useOnboardingStore.getState()).toMatchObject({
            status: null,
            error: "Could not reach the API",
        });
    });

    it("forgets everything on clear", () => {
        useOnboardingStore.setState({ status, error: "x" });

        useOnboardingStore.getState().clear();

        expect(useOnboardingStore.getState()).toMatchObject({ status: null, error: "" });
    });
});