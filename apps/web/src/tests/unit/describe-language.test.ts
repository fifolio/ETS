import { describe, expect, it } from "vitest";

import { describeLanguage } from "@/lib/language/describe-language";

describe("describeLanguage", () => {
    it("shows a translated language by its name", () => {
        const english = { code: "en", name: "English", native_name: "English", direction: "ltr", translated: true };

        expect(describeLanguage(english)).toBe("English");
    });

    it("shows the native name first and marks a language that isn't translated yet", () => {
        const arabic = { code: "ar", name: "Arabic", native_name: "العربية", direction: "rtl", translated: false };

        expect(describeLanguage(arabic)).toBe("العربية (Arabic) - coming soon");
    });

    it("doesn't mark a translated language", () => {
        const french = { code: "fr", name: "French", native_name: "Français", direction: "ltr", translated: true };

        expect(describeLanguage(french)).toBe("Français (French)");
    });
});