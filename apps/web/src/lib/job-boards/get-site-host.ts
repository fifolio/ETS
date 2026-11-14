export function getSiteHost(url: URL): string {
    return url.hostname.toLowerCase().replace(/^www\./, "");
}