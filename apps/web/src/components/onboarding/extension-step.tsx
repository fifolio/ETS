"use client";

import { DEV_TOOLS_ENABLED, EXTENSION_DOWNLOAD_URL } from "@/constants/extension";
import { useExtensionPolling } from "@/hooks/use-extension-polling";
import { useAuthStore } from "@/stores/auth/auth-store";

import { DevExtensionButton } from "./dev-extension-button";

export function ExtensionStep() {
    const email = useAuthStore((state) => state.user?.email);
    useExtensionPolling(true);

    return (
        <div>
            <h2>Install the ETS extension</h2>
            <ol>
                <li>
                    {EXTENSION_DOWNLOAD_URL ? (
                        <a href={EXTENSION_DOWNLOAD_URL}>Download the extension</a>
                    ) : (
                        "The extension is not published yet."
                    )}
                </li>
                <li>Open the extension and log in with {email}.</li>
            </ol>
            <p>This page continues by itself as soon as the extension is logged in.</p>
            {DEV_TOOLS_ENABLED && <DevExtensionButton />}
        </div>
    );
}