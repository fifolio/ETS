"use client";

import {
    MAX_COUNTRY_LENGTH,
    MAX_NAME_LENGTH,
    MAX_NOTES_LENGTH,
    MAX_URL_LENGTH,
} from "@/constants/suggestions";
import { useSuggestionForm } from "@/hooks/use-suggestion-form";
import { describeRemaining } from "@/lib/job-boards/describe-remaining";

export function SuggestJobBoardForm() {
    const { receipt, version, busy, error, handleSubmit } = useSuggestionForm();

    return (
        <form key={version} onSubmit={handleSubmit}>
            <label>
                Job board name <input name="name" required maxLength={MAX_NAME_LENGTH} />
            </label>
            <br />
            <label>
                Main address of its job section (for example https://www.indeed.com/jobs){" "}
                <input name="url" type="url" required maxLength={MAX_URL_LENGTH} />
            </label>
            <br />
            <label>
                A link to one job post on it (helps us a lot){" "}
                <input name="exampleUrl" type="url" required maxLength={MAX_URL_LENGTH} />
            </label>
            <br />
            <label>
                Country or region <input name="country" required maxLength={MAX_COUNTRY_LENGTH} />
            </label>
            <br />
            <label>
                Anything else we should know (optional){" "}
                <textarea name="notes" maxLength={MAX_NOTES_LENGTH} rows={3} />
            </label>
            <br />
            <button type="submit" disabled={busy}>
                Send suggestion
            </button>
            {receipt && (
                <p>
                    Thank you! We will review it. {describeRemaining(receipt.remaining_today)}
                </p>
            )}
            {error && <p role="alert">{error}</p>}
        </form>
    );
}