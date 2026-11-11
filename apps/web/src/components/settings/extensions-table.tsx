import type { ExtensionsTableProps } from "@/types/extension";

import { ExtensionRow } from "./extension-row";

export function ExtensionsTable({ extensions, onRemove }: ExtensionsTableProps) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Browser</th>
                    <th>System</th>
                    <th>Extension</th>
                    <th>Installed</th>
                    <th>Last used</th>
                    <th>Scans</th>
                    <th />
                </tr>
            </thead>
            <tbody>
                {extensions.map((extension) => (
                    <ExtensionRow key={extension.id} extension={extension} onRemove={onRemove} />
                ))}
            </tbody>
        </table>
    );
}