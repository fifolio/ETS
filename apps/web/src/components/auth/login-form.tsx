"use client";

import { useRouter } from "next/navigation";

import { useFormSubmit } from "@/hooks/use-form-submit";
import { useRedirectIfLoggedIn } from "@/hooks/use-redirect-if-logged-in";
import { useAuthStore } from "@/stores/auth/auth-store";

export function LoginForm() {
    const router = useRouter();
    const logIn = useAuthStore((state) => state.logIn);
    useRedirectIfLoggedIn("/dashboard");

    const { busy, error, handleSubmit } = useFormSubmit(async (data) => {
        await logIn({ email: String(data.get("email")), password: String(data.get("password")) });
        router.push("/dashboard");
    });

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Email <input name="email" type="email" required autoComplete="email" />
            </label>
            <br />
            <label>
                Password <input name="password" type="password" required autoComplete="current-password" />
            </label>
            <br />
            <button type="submit" disabled={busy}>
                Log in
            </button>
            {error && <p role="alert">{error}</p>}
        </form>
    );
}