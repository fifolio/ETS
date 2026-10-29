import { beforeEach, describe, expect, it, vi } from "vitest";

const services = vi.hoisted(() => ({
    loadSession: vi.fn(),
    signUp: vi.fn(),
    logIn: vi.fn(),
    logOut: vi.fn(),
}));

vi.mock("@/services/auth/load-session", () => ({ loadSession: services.loadSession }));
vi.mock("@/services/auth/sign-up", () => ({ signUp: services.signUp }));
vi.mock("@/services/auth/log-in", () => ({ logIn: services.logIn }));
vi.mock("@/services/auth/log-out", () => ({ logOut: services.logOut }));

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
    });

    it("passes the error on and keeps no user when log in fails", async () => {
        services.logIn.mockRejectedValue(new Error("Invalid credentials"));

        await expect(
            useAuthStore.getState().logIn({ email: "jane.doe@example.com", password: "wrong-password" }),
        ).rejects.toThrow("Invalid credentials");
        expect(useAuthStore.getState().user).toBeNull();
    });
});