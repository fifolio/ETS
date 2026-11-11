export interface InstalledExtension {
    id: string;
    browser: string | null;
    browser_version: string | null;
    os: string | null;
    extension_version: string | null;
    installed_at: string | null;
    last_used_at: string | null;
    scan_count: number;
}

export interface ExtensionRowProps {
    extension: InstalledExtension;
    onRemove: (id: string) => void;
}

export interface ExtensionsTableProps {
    extensions: InstalledExtension[];
    onRemove: (id: string) => void;
}