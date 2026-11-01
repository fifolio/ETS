"use client";

import { useCvStore } from "@/stores/cv/cv-store";

export function CvStatus() {
    const info = useCvStore((state) => state.info);

    if (!info) {
        return <p>No CV uploaded yet.</p>;
    }
    return (
        <p>
            Current CV: {info.file_name ?? "your CV"} ({info.characters} characters of text)
        </p>
    );
}