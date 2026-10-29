"use client";

import { useState } from "react";

import { checkApiConnection } from "@/services/diagnostics/check-api-connection";

export function ApiCheckButton() {
    const [status, setStatus] = useState("");

    async function handleClick() {
        setStatus(await checkApiConnection());
    }

    return (
        <>
            <button type="button" onClick={handleClick}>
                Check API connection
            </button>
            {status && <p>{status}</p>}
        </>
    );
}