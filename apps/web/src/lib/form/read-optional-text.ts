/** The trimmed text of a form field, or null when it is empty. */
export function readOptionalText(value: FormDataEntryValue | null): string | null {
    const text = String(value ?? "").trim();
    return text === "" ? null : text;
}