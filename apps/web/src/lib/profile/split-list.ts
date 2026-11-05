/** Split text on commas and new lines, trim each item, and drop blanks and duplicates. */
export function splitList(text: string): string[] {
    const items = text
        .split(/[,\n]/)
        .map((item) => item.trim())
        .filter(Boolean);
    return [...new Set(items)];
}