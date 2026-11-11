"use client";

import { useState } from "react";

import { useFormSubmit } from "@/hooks/use-form-submit";
import { validateNewPassword } from "@/lib/account/validate-new-password";
import { changePassword } from "@/services/auth/change-password";

export function ChangePasswordForm() {
    const [version, setVersion] = useState(0);
    const [done, setDone] = useState(false);

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        setDone(false);
        const oldPassword = String(data.get("oldPassword") ?? "");
        const newPassword = String(data.get("newPassword") ?? "");
        const confirmation = String(data.get("confirmPassword") ?? "");

        const problem = validateNewPassword(oldPassword, newPassword, confirmation);
        if (problem) {
            throw new Error(problem);
        }
        await changePassword(oldPassword, newPassword);
        setVersion((value) => value + 1); // a new key empties the form
        setDone(true);
    });

    return (
        <form key={version} onSubmit={handleSubmit}>
            <label>
                Current password{" "}
                <input name="oldPassword" type="password" required autoComplete="current-password" />
            </label>
            <br />
            <label>
                New password{" "}
                <input name="newPassword" type="password" required minLength={8} autoComplete="new-password" />
            </label>
            <br />
            <label>
                Repeat the new password{" "}
                <input name="confirmPassword" type="password" required autoComplete="new-password" />
            </label>
            <br />
            <button type="submit" disabled={busy}>
                Change password
            </button>
            {done && <p>Your password was changed.</p>}
            {error && <p role="alert">{error}</p>}
        </form>
    );
}