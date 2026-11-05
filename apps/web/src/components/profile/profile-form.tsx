"use client";

import { useState } from "react";

import { CheckboxGroup } from "@/components/form/checkbox-group";
import { CURRENCIES } from "@/constants/currencies";
import { EMPLOYMENT_TYPES } from "@/constants/employment-types";
import { ROLE_SUGGESTIONS } from "@/constants/role-suggestions";
import { SENIORITY_LEVELS } from "@/constants/seniority-levels";
import { WORK_ARRANGEMENTS } from "@/constants/work-arrangements";
import { useFormSubmit } from "@/hooks/use-form-submit";
import { parseProfileForm } from "@/lib/profile/parse-profile-form";
import { readProfilePrefs } from "@/lib/profile/read-profile-prefs";
import { saveProfile } from "@/services/profile/save-profile";
import { useAuthStore } from "@/stores/auth/auth-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";

export function ProfileForm() {
    const user = useAuthStore((state) => state.user);
    const refresh = useAuthStore((state) => state.refresh);
    const loadOnboarding = useOnboardingStore((state) => state.load);
    const [saved, setSaved] = useState(false);

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        if (!user) {
            return;
        }
        setSaved(false);
        await saveProfile(user.prefs, parseProfileForm(data));
        await refresh();
        await loadOnboarding();
        setSaved(true);
    });

    if (!user) {
        return null;
    }
    const current = readProfilePrefs(user);

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Role <input name="role" list="role-suggestions" required defaultValue={current.role} />
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
            <label>
                Years of experience{" "}
                <input
                    name="yearsOfExperience"
                    type="number"
                    min={0}
                    max={60}
                    step={1}
                    required
                    defaultValue={current.yearsOfExperience ?? ""}
                />
            </label>
            <br />
            <label>
                Current location (city, country){" "}
                <input name="currentLocation" required defaultValue={current.currentLocation} />
            </label>
            <br />
            <label>
                Desired locations (separate several with commas){" "}
                <textarea
                    name="desiredLocations"
                    required
                    defaultValue={current.desiredLocations.join(", ")}
                />
            </label>
            <br />
            <CheckboxGroup
                name="workArrangements"
                legend="Work arrangement (choose at least one)"
                options={WORK_ARRANGEMENTS}
                selected={current.workArrangements}
            />
            <CheckboxGroup
                name="employmentTypes"
                legend="Employment type (choose at least one)"
                options={EMPLOYMENT_TYPES}
                selected={current.employmentTypes}
            />
            <label>
                <input name="willingToRelocate" type="checkbox" defaultChecked={current.willingToRelocate} />{" "}
                I am willing to relocate
            </label>
            <br />
            <label>
                Expected hourly rate (optional){" "}
                <input
                    name="hourlyRate"
                    type="number"
                    min={0}
                    step={0.01}
                    defaultValue={current.hourlyRate ?? ""}
                />
            </label>{" "}
            <select name="currency" defaultValue={current.currency} aria-label="Currency">
                {CURRENCIES.map((code) => (
                    <option key={code} value={code}>
                        {code}
                    </option>
                ))}
            </select>
            <br />
            <button type="submit" disabled={busy}>
                Save
            </button>
            {saved && <p>Saved.</p>}
            {error && <p role="alert">{error}</p>}
        </form>
    );
}