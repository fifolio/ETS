export function parseOptionalNumber(text: string): number | null {
    if (text.trim() === "") {
        return null;
    }
    const value = Number(text);
    return Number.isFinite(value) ? value : null;
}