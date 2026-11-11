"use client";

import { useState } from "react";

import { useLoadExtensions } from "@/hooks/use-load-extensions";
import { useExtensionsStore } from "@/stores/extension/extensions-store";

import { ExtensionsTable } from "./extensions-table";

export function ExtensionsSection() {
    const items = useExtensionsStore((state) => state.items);
    const remove = useExtensionsStore((state) => state.remove);
    const { loaded, error } = useLoadExtensions();
    const [actionError, setActionError] = useState("");

    async function handleRemove(id: string) {
        const message =
            items.length === 1
                ? "Remove this extension? It is your only one, so you will be asked to log in with the extension again."
                : "Remove this extension? It stops working until you log in with it again.";
        if (!window.confirm(message)) {
            return;
        }
        setActionError("");
        try {
            await remove(id);
        } catch (err) {
            setActionError(err instanceof Error ? err.message : "Could not remove the extension.");
        }
    }

    return (
        <section>
            <h2>Extensions</h2>
            {error && <p role="alert">{error}</p>}
            {!loaded && !error && <p>Loading...</p>}
            {loaded && !error && items.length === 0 && <p>No extensions installed yet.</p>}
            {items.length > 0 && <ExtensionsTable extensions={items} onRemove={handleRemove} />}
            {actionError && <p role="alert">{actionError}</p>}
        </section>
    );
}