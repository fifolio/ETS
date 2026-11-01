import { useState } from "react";
import type { SubmitEvent } from "react";

import { describeUploadError } from "@/lib/cv/describe-upload-error";
import { useCvStore } from "@/stores/cv/cv-store";

export function useCvUpload() {
    const upload = useCvStore((state) => state.upload);
    const [busy, setBusy] = useState(false);
    const [problems, setProblems] = useState<string[]>([]);

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        const form = event.currentTarget;
        const file = new FormData(form).get("file");
        if (!(file instanceof File) || file.size === 0) {
            setProblems(["Choose a PDF file first."]);
            return;
        }

        setBusy(true);
        setProblems([]);
        try {
            await upload(file);
            form.reset();
        } catch (error) {
            setProblems(describeUploadError(error));
        } finally {
            setBusy(false);
        }
    }

    return { busy, problems, handleSubmit };
}