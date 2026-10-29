"use client";

import { useRouter } from "next/navigation";

import { useFormSubmit } from "@/hooks/use-form-submit";
import { useAuthStore } from "@/stores/auth/auth-store";

export function SignUpForm() {
    const router = useRouter();
    const signUp = useAuthStore((state) => state.signUp);

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        await signUp({
            name: String(data.get("name")),
            email: String(data.get("email")),
            password: String(data.get("password")),
        });
        router.push("/profile");
    });

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Name <input name="name" required autoComplete="name" />
            </label>
            <br />
            <label>
                Email <input name="email" type="email" required autoComplete="email" />
            </label>
            <br />
            <label>
                Password{" "}
                <input name="password" type="password" required minLength={8} autoComplete="new-password" />
            </label>
            <br />
            <button type="submit" disabled={busy}>
                Create account
            </button>
            {error && <p role="alert">{error}</p>}
        </form>
    );
}