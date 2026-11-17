import Link from "next/link";

import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <main>
      <h1>Log in</h1>
      <LoginForm />
      <p><a href="/forgot-password">Forgot your password?</a></p>
      <p>
        No account yet? <Link href="/signup">Sign up</Link>
      </p>
    </main>
  );
}