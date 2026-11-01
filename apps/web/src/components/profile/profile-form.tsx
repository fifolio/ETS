"use client";

import { useState } from "react";

import { ROLE_SUGGESTIONS } from "@/constants/role-suggestions";
import { SENIORITY_LEVELS } from "@/constants/seniority-levels";
import { useFormSubmit } from "@/hooks/use-form-submit";
import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import { saveProfile } from "@/services/profile/save-profile";
import { useAuthStore } from "@/stores/auth/auth-store";
import type { SeniorityLevel } from "@/types/profile";

export function ProfileForm() {
    const user = useAuthStore((state) => state.user);
    const refresh = useAuthStore((state) => state.refresh);
    const [saved, setSaved] = useState(false);

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        if (!user) {
            return;
        }
        setSaved(false);
        await saveProfile(user.prefs, {
            role: String(data.get("role")).trim(),
            seniority: String(data.get("seniority")) as SeniorityLevel,
        });
        await refresh();
        setSaved(true);
    });

    if (!user) {
        return null;
    }
    const current = readProfilePrefs(user);

    return (
        <form onSubmit={handleSubmit}>
            <h2>Target role</h2>
            <label>
                Role{" "}
                <input name="role" list="role-suggestions" required defaultValue={current.role} />
            </label>
            <datalist id="role-suggestions">
                {ROLE_SUGGESTIONS.map((role) => (
                    <option key={role} value={role} />
                ))}
            </datalist>
            <br />
            <label>
                Seniority{" "}
                <select name="seniority" required defaultValue={current.seniority}>
                    <option value="">Choose...</option>
                    {SENIORITY_LEVELS.map(({ value, label }) => (
                        <option key={value} value={value}>
                            {label}
                        </option>
                    ))}
                </select>
            </label>
            <br />
            <button type="submit" disabled={busy}>
                Save
            </button>
            {saved && <p>Saved.</p>}
            {error && <p role="alert">{error}</p>}
        </form>
    );
}