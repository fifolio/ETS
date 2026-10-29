import Link from "next/link";

import { SignUpForm } from "@/components/auth/sign-up-form";

export default function SignUpPage() {
  return (
    <main>
      <h1>Sign up</h1>
      <p>Use the same name and email as on your CV.</p>
      <SignUpForm />
      <p>
        Already have an account? <Link href="/login">Log in</Link>
      </p>
    </main>
  );
}