"use client";

import { useState } from "react";

import { useCvStore } from "@/stores/cv/cv-store";

export function DeleteCvButton() {
    const remove = useCvStore((state) => state.remove);
    const [error, setError] = useState("");

    async function handleClick() {
        if (!window.confirm("Delete your CV? You will need to upload it again to scan jobs.")) {
            return;
        }
        setError("");
        try {
            await remove();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not delete the CV.");
        }
    }

    return (
        <>
            <button type="button" onClick={handleClick}>
                Delete my CV
            </button>
            {error && <p role="alert">{error}</p>}
        </>
    );
}