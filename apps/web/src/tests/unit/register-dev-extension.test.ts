import { beforeEach, describe, expect, it, vi } from "vitest";

const { apiFetch } = vi.hoisted(() => ({ apiFetch: vi.fn() }));

vi.mock("@/lib/api/api-fetch", () => ({ apiFetch }));
vi.mock("@/lib/dev/get-dev-install-id", () => ({ getDevInstallId: () => "dev-install-12345" }));

import { registerDevExtension } from "@/services/extensions/register-dev-extension";

beforeEach(() => {
    apiFetch.mockReset();
});

describe("registerDevExtension", () => {
    it("posts the registration of a simulated install to /extensions", async () => {
        apiFetch.mockResolvedValue(new Response('{"created":true}', { status: 201 }));

        await registerDevExtension();

        const [path, init] = apiFetch.mock.calls[0];
        expect(path).toBe("/extensions");
        expect(init.method).toBe("POST");
        expect(JSON.parse(init.body)).toMatchObject({
            install_id: "dev-install-12345",
            browser: "Chrome (dev simulator)",
        });
    });

    it("throws the API's message when the registration is refused", async () => {
        apiFetch.mockResolvedValue(
            new Response(JSON.stringify({ detail: "Verify your email first." }), { status: 403 }),
        );

        await expect(registerDevExtension()).rejects.toThrow("Verify your email first.");
    });
});