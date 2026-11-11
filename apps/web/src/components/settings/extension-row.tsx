import { formatDateTime } from "@/lib/format/format-date-time";
import type { ExtensionRowProps } from "@/types/extension";

export function ExtensionRow({ extension, onRemove }: ExtensionRowProps) {
    const browser =
        [extension.browser, extension.browser_version].filter(Boolean).join(" ") || "Unknown";

    return (
        <tr>
            <td>{browser}</td>
            <td>{extension.os || "Unknown"}</td>
            <td>{extension.extension_version || "Unknown"}</td>
            <td>{formatDateTime(extension.installed_at, "Unknown")}</td>
            <td>{formatDateTime(extension.last_used_at, "Never")}</td>
            <td>{extension.scan_count}</td>
            <td>
                <button type="button" onClick={() => onRemove(extension.id)}>
                    Remove
                </button>
            </td>
        </tr>
    );
}