/** A public-looking web address as a URL, or null for anything else. */
export function parseWebAddress(text: string): URL | null {
    try {
        const url = new URL(text.trim());
        const isWeb = url.protocol === "http:" || url.protocol === "https:";
        return isWeb && url.hostname.includes(".") && !url.username && !url.password ? url : null;
    } catch {
        return null;
    }
}