import { describe, expect, it } from "vitest";

import { validateNewPassword } from "@/lib/account/validate-new-password";

describe("validateNewPassword", () => {
    it("accepts a valid change", () => {
        expect(validateNewPassword("old-password", "new-password-1", "new-password-1")).toBeNull();
    });

    it("asks for the current password", () => {
        expect(validateNewPassword("", "new-password-1", "new-password-1")).toMatch(/current password/);
    });

    it("rejects a new password that is too short", () => {
        expect(validateNewPassword("old-password", "short", "short")).toMatch(/at least 8/);
    });

    it("rejects a confirmation that doesn't match", () => {
        expect(validateNewPassword("old-password", "new-password-1", "new-password-2")).toMatch(
            /don't match/,
        );
    });

    it("rejects a new password equal to the current one", () => {
        expect(validateNewPassword("same-password", "same-password", "same-password")).toMatch(
            /different/,
        );
    });
});