import { beforeEach, describe, expect, it, vi } from "vitest";

const { updatePassword } = vi.hoisted(() => ({ updatePassword: vi.fn() }));

vi.mock("@/lib/appwrite", () => ({ account: { updatePassword } }));

import { changePassword } from "@/services/auth/change-password";

beforeEach(() => {
    updatePassword.mockReset();
});

describe("changePassword", () => {
    it("sends the new and the current password to Appwrite", async () => {
        updatePassword.mockResolvedValue({});

        await changePassword("old-password", "new-password-1");

        expect(updatePassword).toHaveBeenCalledWith({
            password: "new-password-1",
            oldPassword: "old-password",
        });
    });

    it("passes Appwrite's error on, for example a wrong current password", async () => {
        updatePassword.mockRejectedValue(new Error("Invalid credentials."));

        await expect(changePassword("wrong", "new-password-1")).rejects.toThrow("Invalid credentials.");
    });
});