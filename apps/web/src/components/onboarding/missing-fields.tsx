import { PROFILE_FIELD_LABELS } from "@/constants/profile-field-labels";
import type { MissingFieldsProps } from "@/types/onboarding/onboarding";

export function MissingFields({ fields }: MissingFieldsProps) {
    if (fields.length === 0) {
        return null;
    }
    const labels = [...new Set(fields.map((field) => PROFILE_FIELD_LABELS[field] ?? field))];
    return (
        <p role="alert">
            Still missing: {labels.join(", ")}
        </p>
    );
}