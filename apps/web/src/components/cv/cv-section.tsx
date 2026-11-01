"use client";

import { useLoadCv } from "@/hooks/use-load-cv";
import { useCvStore } from "@/stores/cv/cv-store";

import { CvStatus } from "./cv-status";
import { CvUploadForm } from "./cv-upload-form";
import { DeleteCvButton } from "./delete-cv-button";

export function CvSection() {
    const info = useCvStore((state) => state.info);
    const { loaded, error } = useLoadCv();

    return (
        <section>
            <h2>CV</h2>
            {error && <p role="alert">{error}</p>}
            {!loaded && !error && <p>Loading...</p>}
            {loaded && (
                <>
                    <CvStatus />
                    <CvUploadForm hasCv={info !== null} />
                    {info && <DeleteCvButton />}
                </>
            )}
        </section>
    );
}