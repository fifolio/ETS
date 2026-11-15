import { beforeEach, describe, expect, it, vi } from "vitest";

const { updatePrefs } = vi.hoisted(() => ({ updatePrefs: vi.fn() }));

vi.mock("@/lib/appwrite", () => ({ account: { updatePrefs } }));

import { saveAccountPrefs } from "@/services/account/save-account-prefs";

beforeEach(() => {
    updatePrefs.mockReset();
});

describe("saveAccountPrefs", () => {
    it("saves the change and keeps every other preference", async () => {
        updatePrefs.mockResolvedValue({});

        await saveAccountPrefs({ theme: "light", language: "en", role: "Nurse" }, { theme: "dark" });

        expect(updatePrefs).toHaveBeenCalledWith({
            prefs: { theme: "dark", language: "en", role: "Nurse" },
        });
    });

    it("passes Appwrite's error on", async () => {
        updatePrefs.mockRejectedValue(new Error("Could not save"));

        await expect(saveAccountPrefs({}, { language: "fr" })).rejects.toThrow("Could not save");
    });
});