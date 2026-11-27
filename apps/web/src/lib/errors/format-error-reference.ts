/** A short line the user can quote to support, or nothing when Next gave no reference. */
export function formatErrorReference(digest?: string): string {
    return digest ? `Reference: ${digest}` : "";
}