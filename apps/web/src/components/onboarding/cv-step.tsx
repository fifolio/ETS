import { CvUploadForm } from "@/components/cv/cv-upload-form";

export function CvStep() {
    return (
        <div>
            <h2>Upload your CV</h2>
            <p>Your CV must contain the same name and email as your account.</p>
            <CvUploadForm hasCv={false} />
        </div>
    );
}