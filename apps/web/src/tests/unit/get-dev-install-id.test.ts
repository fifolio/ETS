import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { getDevInstallId } from "@/lib/dev/get-dev-install-id";

function fakeStorage(initial: Record<string, string> = {}) {
    const data = { ...initial };
    return {
        getItem: (key: string) => data[key] ?? null,
        setItem: (key: string, value: string) => {
            data[key] = value;
        },
        data,
    };
}

let storage = fakeStorage();

beforeEach(() => {
    storage = fakeStorage();
    vi.stubGlobal("window", { localStorage: storage });
});

afterEach(() => {
    vi.unstubAllGlobals();
});

describe("getDevInstallId", () => {
    it("creates an id on the first call and saves it", () => {
        const id = getDevInstallId();

        expect(id).toMatch(/^[0-9a-f-]{36}$/);
        expect(storage.data["ets-dev-install-id"]).toBe(id);
    });

    it("returns the saved id on later calls", () => {
        storage = fakeStorage({ "ets-dev-install-id": "saved-id-123456" });
        vi.stubGlobal("window", { localStorage: storage });

        expect(getDevInstallId()).toBe("saved-id-123456");
    });
});