"use client";

import { useDeleteAccount } from "@/hooks/use-delete-account";
import { useAuthStore } from "@/stores/auth/auth-store";

export function DeleteAccountSection() {
    const email = useAuthStore((state) => state.user?.email ?? "");
    const { confirmation, setConfirmation, busy, error, handleDelete } = useDeleteAccount();
    const matches = email !== "" && confirmation.trim().toLowerCase() === email.toLowerCase();

    return (
        <section>
            <h2>Delete account</h2>
            <p>
                This deletes your CV, scans, usage totals, and extensions, then your account. It can not be
                undone. A testimonial you already sent is kept.
            </p>
            <label>
                Type your email ({email}) to confirm{" "}
                <input value={confirmation} onChange={(event) => setConfirmation(event.target.value)} />
            </label>{" "}
            <button type="button" onClick={handleDelete} disabled={!matches || busy}>
                Delete my account
            </button>
            {error && <p role="alert">{error}</p>}
        </section>
    );
}