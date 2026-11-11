import { beforeEach, describe, expect, it, vi } from "vitest";

const services = vi.hoisted(() => ({
    getExtensions: vi.fn(),
    removeExtension: vi.fn(),
    loadOnboarding: vi.fn(),
}));

vi.mock("@/services/extensions/get-extensions", () => ({ getExtensions: services.getExtensions }));
vi.mock("@/services/extensions/remove-extension", () => ({
    removeExtension: services.removeExtension,
}));
vi.mock("@/stores/onboarding/onboarding-store", () => ({
    useOnboardingStore: { getState: () => ({ load: services.loadOnboarding }) },
}));

import { useExtensionsStore } from "@/stores/extension/extensions-store";

const item = {
    id: "ext-1",
    browser: "Chrome",
    browser_version: "130",
    os: "Windows",
    extension_version: "0.1.0",
    installed_at: null,
    last_used_at: null,
    scan_count: 2,
};

beforeEach(() => {
    vi.resetAllMocks();
    useExtensionsStore.setState({ items: [], loaded: false, error: "" });
});

describe("extensions store", () => {
    it("stores the installs from the API", async () => {
        services.getExtensions.mockResolvedValue([item]);

        await useExtensionsStore.getState().load();

        expect(useExtensionsStore.getState()).toMatchObject({ items: [item], loaded: true, error: "" });
    });

    it("keeps an error message when loading fails", async () => {
        services.getExtensions.mockRejectedValue(new Error("API down"));

        await useExtensionsStore.getState().load();

        expect(useExtensionsStore.getState()).toMatchObject({ loaded: true, error: "API down" });
    });

    it("removes an install, reloads the list, and refreshes the setup status", async () => {
        services.removeExtension.mockResolvedValue(undefined);
        services.getExtensions.mockResolvedValue([]);

        await useExtensionsStore.getState().remove("ext-1");

        expect(services.removeExtension).toHaveBeenCalledWith("ext-1");
        expect(services.getExtensions).toHaveBeenCalledTimes(1);
        expect(services.loadOnboarding).toHaveBeenCalledTimes(1);
    });

    it("passes the error on and keeps the list when removing fails", async () => {
        useExtensionsStore.setState({ items: [item], loaded: true });
        services.removeExtension.mockRejectedValue(new Error("Could not remove"));

        await expect(useExtensionsStore.getState().remove("ext-1")).rejects.toThrow("Could not remove");
        expect(useExtensionsStore.getState().items).toEqual([item]);
    });

    it("forgets everything on clear", () => {
        useExtensionsStore.setState({ items: [item], loaded: true, error: "x" });

        useExtensionsStore.getState().clear();

        expect(useExtensionsStore.getState()).toMatchObject({ items: [], loaded: false, error: "" });
    });
});