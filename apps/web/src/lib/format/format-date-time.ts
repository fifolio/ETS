export function formatDateTime(
    value: string | null,
    emptyText = "Unknown",
    timeZone?: string,
): string {
    if (!value) {
        return emptyText;
    }
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return "Unknown";
    }
    return new Intl.DateTimeFormat("en-US", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone,
    }).format(date);
}