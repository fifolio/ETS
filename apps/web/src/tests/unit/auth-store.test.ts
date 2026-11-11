import { beforeEach, describe, expect, it, vi } from "vitest";

const services = vi.hoisted(() => ({
    loadSession: vi.fn(),
    signUp: vi.fn(),
    logIn: vi.fn(),
    logOut: vi.fn(),
    clearCv: vi.fn(),
    clearOnboarding: vi.fn(),
    clearFeedback: vi.fn(),
    clearExtensions: vi.fn()
}));

vi.mock("@/services/auth/load-session", () => ({ loadSession: services.loadSession }));
vi.mock("@/services/auth/sign-up", () => ({ signUp: services.signUp }));
vi.mock("@/services/auth/log-in", () => ({ logIn: services.logIn }));
vi.mock("@/services/auth/log-out", () => ({ logOut: services.logOut }));
vi.mock("@/stores/cv/cv-store", () => ({
    useCvStore: { getState: () => ({ clear: services.clearCv }) },
}));
vi.mock("@/stores/onboarding/onboarding-store", () => ({
    useOnboardingStore: { getState: () => ({ clear: services.clearOnboarding }) },
}));
vi.mock("@/stores/feedback/feedback-store", () => ({
    useFeedbackStore: { getState: () => ({ clear: services.clearFeedback }) },
}));
vi.mock("@/stores/extension/extensions-store", () => ({
    useExtensionsStore: { getState: () => ({ clear: services.clearExtensions }) },
}));

import { useAuthStore } from "@/stores/auth/auth-store";
import type { AppUser } from "@/types/auth/auth";

const jane = { $id: "user-1", name: "Jane Doe", email: "jane.doe@example.com" } as AppUser;

beforeEach(() => {
    vi.resetAllMocks();
    useAuthStore.setState({ user: null, loading: true });
});

describe("auth store", () => {
    it("stores the user and stops loading when a session exists", async () => {
        services.loadSession.mockResolvedValue(jane);

        await useAuthStore.getState().loadSession();

        expect(useAuthStore.getState()).toMatchObject({ user: jane, loading: false });
    });

    it("ends with no user and stops loading when nobody is logged in", async () => {
        services.loadSession.mockResolvedValue(null);

        await useAuthStore.getState().loadSession();

        expect(useAuthStore.getState()).toMatchObject({ user: null, loading: false });
    });

    it("stores the new user after sign up", async () => {
        services.signUp.mockResolvedValue(jane);

        await useAuthStore.getState().signUp({ name: "Jane Doe", email: "jane.doe@example.com", password: "password1" });

        expect(useAuthStore.getState().user).toEqual(jane);
    });

    it("stores the user after log in", async () => {
        services.logIn.mockResolvedValue(jane);

        await useAuthStore.getState().logIn({ email: "jane.doe@example.com", password: "password1" });

        expect(useAuthStore.getState().user).toEqual(jane);
    });

    it("clears the user after log out", async () => {
        useAuthStore.setState({ user: jane, loading: false });
        services.logOut.mockResolvedValue(undefined);

        await useAuthStore.getState().logOut();

        expect(useAuthStore.getState().user).toBeNull();
        expect(services.clearCv).toHaveBeenCalled();
        expect(services.clearOnboarding).toHaveBeenCalled();
        expect(services.clearFeedback).toHaveBeenCalled();
        expect(services.clearExtensions).toHaveBeenCalled();
    });

    it("passes the error on and keeps no user when log in fails", async () => {
        services.logIn.mockRejectedValue(new Error("Invalid credentials"));

        await expect(
            useAuthStore.getState().logIn({ email: "jane.doe@example.com", password: "wrong-password" }),
        ).rejects.toThrow("Invalid credentials");
        expect(useAuthStore.getState().user).toBeNull();
    });

    it("forgets the user locally without calling the log out service", () => {
        useAuthStore.setState({ user: jane, loading: false });

        useAuthStore.getState().signOutLocally();

        expect(useAuthStore.getState().user).toBeNull();
        expect(services.logOut).not.toHaveBeenCalled();
        expect(services.clearCv).toHaveBeenCalled();
    });
});