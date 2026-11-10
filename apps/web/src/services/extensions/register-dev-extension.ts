import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import { getDevInstallId } from "@/lib/dev/get-dev-install-id";
import type { ExtensionRegistration } from "@/types/extension";

export async function registerDevExtension(): Promise<void> {
    const registration: ExtensionRegistration = {
        install_id: getDevInstallId(),
        browser: "Chrome (dev simulator)",
        browser_version: "0",
        os: "Dev",
        extension_version: "0.0.0-dev",
    };
    const response = await apiFetch("/extensions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registration),
    });
    if (!response.ok) {
        throw await readApiError(response);
    }
}