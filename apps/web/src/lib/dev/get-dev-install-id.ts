const STORAGE_KEY = "ets-dev-install-id";

/** A stable fake install ID for this browser, used only by the development simulator. */
export function getDevInstallId(): string {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved) {
        return saved;
    }
    const created = crypto.randomUUID();
    window.localStorage.setItem(STORAGE_KEY, created);
    return created;
}