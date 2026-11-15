import type { LanguageInfo } from "@/types/language";

/** The name shown in the language list, marking languages that aren't translated yet. */
export function describeLanguage(language: LanguageInfo): string {
    const label =
        language.native_name === language.name
            ? language.name
            : `${language.native_name} (${language.name})`;
    return language.translated ? label : `${label} - coming soon`;
}