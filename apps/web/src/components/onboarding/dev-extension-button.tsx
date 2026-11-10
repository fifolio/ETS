"use client";

import { useState } from "react";

import { registerDevExtension } from "@/services/extensions/register-dev-extension";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

/** Development only: does what the extension will do after the user logs in. */
export function DevExtensionButton() {
    const load = useOnboardingStore((state) => state.load);
    const [message, setMessage] = useState("");

    async function handleClick() {
        setMessage("");
        try {
            await registerDevExtension();
            await load();
        } catch (err) {
            setMessage(err instanceof Error ? err.message : "Could not register the simulated extension.");
        }
    }

    return (
        <div>
            <p>Development only: the real extension does this by itself after you log in.</p>
            <button type="button" onClick={handleClick}>
                Simulate extension login
            </button>
            {message && <p role="alert">{message}</p>}
        </div>
    );
}