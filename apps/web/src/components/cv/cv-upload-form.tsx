"use client";

import { useCvUpload } from "@/hooks/use-cv-upload";
import type { CvUploadFormProps } from "@/types/cv/cv";

import { ProblemList } from "./problem-list";

export function CvUploadForm({ hasCv }: CvUploadFormProps) {
    const { busy, problems, handleSubmit } = useCvUpload();

    return (
        <form onSubmit={handleSubmit}>
            <label>
                {hasCv ? "Replace your CV" : "Upload your CV"} (PDF, up to 5 MB){" "}
                <input name="file" type="file" accept="application/pdf" required />
            </label>{" "}
            <button type="submit" disabled={busy}>
                {hasCv ? "Replace" : "Upload"}
            </button>
            <ProblemList problems={problems} />
        </form>
    );
}