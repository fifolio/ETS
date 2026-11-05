import { describe, expect, it } from "vitest";

import { readAccountPrefs } from "@/lib/account/read-account-prefs";
import type { AppUser } from "@/types/auth/auth";

const makeUser = (prefs: object) => ({ prefs }) as unknown as AppUser;

describe("readAccountPrefs", () => {
    it("uses light and English when nothing is saved", () => {
        expect(readAccountPrefs(makeUser({}))).toEqual({ theme: "light", language: "en" });
    });

    it("reads saved values", () => {
        expect(readAccountPrefs(makeUser({ theme: "dark", language: "ar" }))).toEqual({
            theme: "dark",
            language: "ar",
        });
    });

    it("falls back to the defaults for unknown values", () => {
        expect(readAccountPrefs(makeUser({ theme: "neon", language: "xx" }))).toEqual({
            theme: "light",
            language: "en",
        });
    });
});