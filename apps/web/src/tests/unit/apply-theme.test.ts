import { describe, expect, it } from "vitest";

import { applyTheme } from "@/lib/theme/apply-theme";

function fakeRoot() {
    return { style: {} as Record<string, string>, dataset: {} as Record<string, string> };
}

describe("applyTheme", () => {
    it("sets the color scheme and a data attribute", () => {
        const root = fakeRoot();

        applyTheme("dark", root as unknown as HTMLElement);

        expect(root.style.colorScheme).toBe("dark");
        expect(root.dataset.theme).toBe("dark");
    });

    it("switches back to light", () => {
        const root = fakeRoot();

        applyTheme("dark", root as unknown as HTMLElement);
        applyTheme("light", root as unknown as HTMLElement);

        expect(root.style.colorScheme).toBe("light");
        expect(root.dataset.theme).toBe("light");
    });
});